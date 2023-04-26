from other_module import CONFIG
from .DbClasses import User, Group, Answer, VkApiToken, Subscription
from .DbCore import core


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

    async def new_group(self, group_id: int, domain: str, last_post_id: int = 0):
        """
        :param group_id: int
        :param domain: str
        :param last_post_id: int = 0
        :return: None
        """
        new_group = Group(id=group_id, domain=domain, last_post_id=last_post_id)
        await self.__add_commit(new_group)

    async def new_answer(self, user_id: int, message: str):
        """
        :param user_id: int
        :param message: str
        :return: None
        """
        new_answer = Answer(user_id=user_id, message=message)
        await self.__add_commit(new_answer)

    async def new_token(self, user_id: int, token: str):
        """
        :param user_id: int
        :param token: str
        :return: None
        """
        new_token = VkApiToken(user_id=user_id, token=token, nickname=self.__standard_token_nickname)
        await self.__add_commit(new_token)

    async def new_subs(self, group_id: int, user_id: int, token_id: int):
        """
        :param group_id: int
        :param user_id: int
        :param token_id: int
        :return: None
        """
        new_subscription = Subscription(group_id=group_id, user_id=user_id, token_id=token_id)
        await self.__add_commit(new_subscription)


creator = Creator()
