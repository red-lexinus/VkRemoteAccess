from sqlalchemy import update

from .DbClasses import User, Group, Answer, VkApiToken
from .DbCore import core


class Updater:
    def __init__(self):
        self.__async_session = core.get_new_async_session()

    async def __update(self, obj):
        await self.__async_session.execute(obj)
        await self.__async_session.commit()

    async def user_time_zone(self, user_id: int, time_zone: int):
        """
        :param user_id: int
        :param time_zone: int
        :return: None
        """
        await self.__update(
            update(User).filter_by(id=user_id).values(time_zone=time_zone)
        )

    async def user_available(self, user_id: int, available: bool):
        """
        :param user_id: int
        :param available: bool
        :return: None
        """
        await self.__update(
            update(User).filter_by(id=user_id).values(available=available)
        )

    async def group_post_id(self, group_id: int, new_post_id: int):
        """
        :param group_id: int
        :param new_post_id: int
        :return: None
        """
        await self.__update(
            update(Group).filter_by(id=group_id).values(last_post_id=new_post_id)
        )

    async def group_serviceable(self, group_id: int, serviceable: bool):
        """
        :param group_id: int
        :param serviceable: bool
        :return: None
        """
        await self.__update(
            update(Group).filter_by(id=group_id).values(serviceable=serviceable)
        )

    async def answer_nickname(self, answer_id: int, new_nickname: str):
        """
        :param answer_id: int
        :param new_nickname: str
        :return: None
        """
        await self.__update(
            update(Answer).filter_by(id=answer_id).values(nickname=new_nickname)
        )

    async def token_nickname(self, token_id: int, new_nickname: str):
        """
        :param token_id: int
        :param new_nickname:str
        :return: None
        """
        await self.__update(
            update(VkApiToken).filter_by(id=token_id).values(nickname=new_nickname)
        )

    async def token_serviceable(self, token_id: int, serviceable: str):
        """
        :param token_id: int
        :param serviceable: bool
        :return: None
        """
        await self.__update(
            update(VkApiToken).filter_by(id=token_id).values(serviceable=serviceable)
        )


updater = Updater()
