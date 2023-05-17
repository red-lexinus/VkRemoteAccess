import asyncio
import time

from aiogram import Bot
from aiogram.types import InputMediaPhoto
from aiogram.exceptions import TelegramRetryAfter
from sqlalchemy.engine.row import Row as SqlalchemyRow

from DbManagerModule import getter, updater, creator, DbClasses
from TgModule.keyboards.inline import get_comment_post_ikb
from VkApiModule.ParseClasses import GroupsUpdated, VkPosts, VkPost
from VkApiModule import vk_parser
from OtherModule import CONFIG


async def get_updated_groups() -> GroupsUpdated:
    datas = await getter.updated_groups()
    res = GroupsUpdated(groups=[])
    for data in datas:
        res.add_group(data)
    return res


async def get_new_posts(groups: GroupsUpdated):
    return await vk_parser.get_groups_posts(groups)


def mailing_handler(func):
    async def _wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except TelegramRetryAfter:
            await asyncio.sleep(60)
            return await func(*args, **kwargs)

    return _wrapper


class Server:
    def __init__(self, bot: Bot):
        self.__bot = bot

    async def startup(self, min_time_iteration: int, first_sleep_time: int = 60):
        await asyncio.sleep(first_sleep_time)
        run = True
        while run:
            first_time = time.time()
            new_posts = await get_new_posts(await get_updated_groups())
            await self.__processing_new_posts(new_posts)
            second_time = time.time()
            if second_time - first_time < min_time_iteration:
                await asyncio.sleep(first_time + min_time_iteration - second_time)

    async def __processing_new_posts(self, new_posts: list[VkPosts]):
        for posts in new_posts:
            group_id = posts.group_id
            if posts.posts:
                data = await getter.group(group_id)
                new_last_post_id = data.last_post_id
                for post in posts.posts:
                    new_last_post_id = max(post.id, new_last_post_id)
                    await self.__save_new_post(group_id, post)
                await updater.group_post_id(group_id=group_id, new_post_id=new_last_post_id)
                await self.__mailing_new_posts(group_id, data.last_post_id)

    async def __save_new_post(self, group_id: int, new_post: VkPost):
        await creator.new_storage_post(None, group_id, new_post.id, 1, new_post.date)
        repost = new_post.get_copy_history()
        await creator.new_storage_post(None, group_id, new_post.id, 2, None)
        await self.__save_chart_post_in_storage(new_post, group_id, new_post.id)
        if repost:
            await creator.new_storage_post(None, group_id, new_post.id, 3, None)
            await self.__save_chart_post_in_storage(repost, group_id, new_post.id)

    async def __save_chart_post_in_storage(self, post: VkPost, group_id: int, main_post_id: int):
        photos = []
        videos = []
        tasks_db_save = []
        for attach in post.attachments:
            if attach.photo:
                photos.append(InputMediaPhoto(media=attach.photo.get_max_photo_size().url))
            elif attach.video:
                videos.append(attach.video.get_video_url())
        text_in_repost = post.text
        if videos:
            text_in_repost += ' '.join(['( url роликов', ' '.join(videos), ")"])
        if photos:
            belated_text = ''
            if len(text_in_repost) > 1020:
                belated_text = text_in_repost[1000:]
                text_in_repost = text_in_repost[:1000]
            photos[-1].caption = text_in_repost
            messages_id = await self.__send_message_to_storage(media=photos)
            tasks_db_save.append(asyncio.create_task(creator.new_storage_post(messages_id[0], group_id, main_post_id)))
            if belated_text:
                messages_id = await self.__send_message_to_storage(message=belated_text)
                tasks_db_save.append(
                    asyncio.create_task(creator.new_storage_post(messages_id[0], group_id, main_post_id)))
        elif text_in_repost:
            messages_id = await self.__send_message_to_storage(message=text_in_repost)
            tasks_db_save.append(asyncio.create_task(creator.new_storage_post(messages_id[0], group_id, main_post_id)))
        else:
            pass
        await asyncio.gather(*tasks_db_save)

    async def __send_message_to_storage(self, message: str = '', media=None,
                                        reply_msg_id: int | None = None) -> list[int]:
        if media:
            msg = await self.__send_media_group_msg(chat_id=CONFIG.TG_DATA_STORAGE_CHANNEL_ID, media=media,
                                                    reply_to_message_id=reply_msg_id)
            return [i.message_id for i in msg]
        elif message:
            msgs = []
            for i in range(len(message) // 4000 + 1):
                msg = await self.__send_msg(chat_id=CONFIG.TG_DATA_STORAGE_CHANNEL_ID,
                                            text=message[i * 4000:(i + 1) * 4000],
                                            reply_to_message_id=reply_msg_id)
                msgs.append(msg.message_id)
            return msgs
        raise "Что отправлять то?"

    async def __mailing_new_posts(self, group_id: int, old_last_post_id: int):
        data = await getter.data_for_mailing_posts(group_id, old_last_post_id)
        users_mailing_tasks: list[asyncio.Task[any]] = []
        for user in data[0]:
            users_mailing_tasks.append(asyncio.create_task(self.__mailing_user(user, data[1], group_id)))
        await asyncio.gather(*users_mailing_tasks)

    async def __mailing_user(self,
                             user_data: SqlalchemyRow[DbClasses.User.id, DbClasses.User.time_zone,
                                                      DbClasses.Subscription.nickname],
                             messages: list[SqlalchemyRow[DbClasses.StoragePosts]],
                             group_id: int):
        post_id = None
        user_answers = await getter.answers_filter(user_id=user_data[0])
        for message_data in messages:
            message = message_data[0]
            if not post_id:
                post_id = message.post_id
            elif post_id != message.post_id:
                await self.__send_comment_msg(user_data[0], group_id, post_id, user_answers)
                post_id = message.post_id
            match message.type_id:
                case 0:
                    await self.__send_copy_msg(chat_id=user_data[0], from_chat_id=CONFIG.TG_DATA_STORAGE_CHANNEL_ID,
                                               message_id=message.storage_id)
                case 1:
                    await self.__send_post_date(user_data[0], int(message.data), user_data[1])
                case 2:
                    await self.__send_msg(chat_id=user_data[0], text=user_data[-1])
                case 3:
                    await self.__send_msg(chat_id=user_data[0], text='Ответ на:')
        await self.__send_comment_msg(user_data[0], group_id, post_id, user_answers)

    async def __send_post_date(self, user_id: int, date: int, utf_time: int):
        user_date = time.gmtime(date + utf_time * 3600)
        msg = f'Дата выхода {user_date.tm_mday}-{user_date.tm_mon}-{user_date.tm_year % 100} ' \
              f'в {user_date.tm_hour}-{user_date.tm_min}'
        await self.__send_msg(chat_id=user_id, text=msg)

    async def __send_comment_msg(self, user_id: int, group_id: int, post_id: int, data):
        reply_markup = get_comment_post_ikb(group_id, post_id, data)
        await self.__send_msg(chat_id=user_id, text='И что-же вы на это ответите?', reply_markup=reply_markup)

    @mailing_handler
    async def __send_msg(self, **kwargs):
        return await self.__bot.send_message(**kwargs)

    @mailing_handler
    async def __send_copy_msg(self, **kwargs):
        return await self.__bot.copy_message(**kwargs)

    @mailing_handler
    async def __send_media_group_msg(self, **kwargs):
        return await self.__bot.send_media_group(**kwargs)
