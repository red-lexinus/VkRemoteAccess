import asyncio

from aiogram import Router, F, Dispatcher, types
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.filters import Text

from DbManagerModule import getter, creator, checker
from VkApiModule import vk_parser, ParseClasses
from TgModule.filters import ChatTypeFilter, InTextFilter
from TgModule.templates import base_message
from TgModule.keyboards import inline

router = Router()
router.message.filter(ChatTypeFilter('private'))


@router.message(F.text, InTextFilter('vk1.a.'))
async def new_group_handler(msg: types.Message) -> None:
    await msg.reply('Затычка')


@router.message(F.text, InTextFilter('vk.com/'))
async def new_group_handler(msg: types.Message) -> None:
    group_domain = url_group_domain(msg.text)
    if group_domain:
        tokens = await getter.tokens_filter(user_id=msg.from_user.id)
        if tokens:
            success_tokens = []
            group_data = None
            for token_data in tokens:
                res = await vk_parser.get_group_info_by_domain(
                    ParseClasses.VkParserGroupDomain(token=token_data[0].token, domain=group_domain)
                )
                if res.id:
                    success_tokens.append(token_data[0])
                    if not group_data:
                        group_data = res
            if group_data:
                await msg.answer_photo(
                    photo=group_data.photo_200, caption=base_message.check_group(group_data), reply_markup=
                    inline.sub_new_group(group_id=group_data.id, group_name=group_data.name, tokens=success_tokens)
                )
            else:
                await msg.reply(base_message.failed_check_group())
        else:
            await msg.reply(base_message.none_token())
    else:
        await msg.reply(base_message.none_group_url())


@router.message(F.text)
async def unknown_handler(msg: types.Message) -> None:
    await msg.reply(base_message.unknown_handler(msg.text))


def url_group_domain(url: str) -> str:
    elements = url.split('vk.com/')
    if elements:
        return elements[-1].split('/')[0]
