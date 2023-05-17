from OtherModule import CONFIG
from DbManagerModule.DbCore import core
from DbManagerModule.DbClasses import (User, Group, Answer, VkApiToken, Subscription, UserRights, StoragePosts)


class Creator:
    def __init__(self):
        self.__async_session = core.get_new_async_session()
        self.__standard_token_nickname = CONFIG.VK_TOKEN_NICKNAME

    async def __add_commit(self, obj):
        self.__async_session.add(obj)
        await self.__async_session.commit()

    async def new_user(self, user_id: int):
        """
        :param user_id: int
        :return: None
        """
        new_user = User(id=user_id)
        await self.__add_commit(new_user)
        await self.__user_rights(user_id)

    async def __user_rights(self, user_id: int):
        """
        :param user_id: int
        :return: None
        """
        new_user_rights = UserRights(
            id=user_id, max_tokens=CONFIG.MAX_TOKENS_DEFAULT, max_subs=CONFIG.MAX_PUBLIC_DEFAULT
        )
        await self.__add_commit(new_user_rights)

    async def new_group(self, group_id: int, domain: str, last_post_id: int = 0):
        """
        :param group_id: int
        :param domain: str
        :param last_post_id: int = 0
        :return: None
        """
        new_group = Group(id=group_id, domain=domain, last_post_id=last_post_id)
        await self.__add_commit(new_group)

    async def new_answer(self, user_id: int, message: str, nickname: str):
        """
        :param user_id: int
        :param message: str
        :param nickname: str
        :return: None
        """
        new_answer = Answer(user_id=user_id, message=message, nickname=nickname)
        await self.__add_commit(new_answer)

    async def new_token(self, user_id: int, token: str):
        """
        :param user_id: int
        :param token: str
        :return: None
        """
        new_token = VkApiToken(user_id=user_id, token=token, nickname=self.__standard_token_nickname)
        await self.__add_commit(new_token)

    async def new_subs(self, group_id: int, user_id: int, token_id: int, nickname: str = "Группа"):
        """
        :param group_id: int
        :param user_id: int
        :param token_id: int
        :param nickname: str
        :return: None
        """
        new_subscription = Subscription(group_id=group_id, user_id=user_id, token_id=token_id, nickname=nickname)
        await self.__add_commit(new_subscription)

    async def new_storage_post(self, storage_id: int or None, group_id: int, post_id: int, type_id: int = 0,
                               data: int or None = None):
        """
        :param storage_id: int or None
        :param group_id: int
        :param post_id: int
        :param type_id: int
        :param data: int or None
        :return: None
        """
        new_storage_post = StoragePosts(storage_id=storage_id, group_id=group_id, post_id=post_id, type_id=type_id,
                                        data=data)
        await self.__add_commit(new_storage_post)


creator = Creator()
