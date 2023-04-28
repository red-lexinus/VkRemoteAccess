from sqlalchemy import update

from .DbClasses import User, Group, Answer, VkApiToken, Base, UserRights
from .DbCore import core


class Updater:
    def __init__(self):
        self.__async_session = core.get_new_async_session()

    async def __update(self, db_class: Base, class_id: int, **kwargs):
        obj = update(db_class).filter_by(id=class_id).values(**kwargs)
        await self.__async_session.execute(obj)
        await self.__async_session.commit()

    async def user_time_zone(self, user_id: int, time_zone: int):
        """
        :param user_id: int
        :param time_zone: int
        :return: None
        """
        await self.__update(User, class_id=user_id, time_zone=time_zone)

    async def user_rights(self, user_id: int, **kwargs):
        """
        :param user_id: int
        :param kwargs:
            'max_tokens': type int
            'max_subs': type int
            'donate': type bool
        :return: None
        """
        await self.__update(UserRights, db_class=user_id, **kwargs)

    async def user_available(self, user_id: int, available: bool):
        """
        :param user_id: int
        :param available: bool
        :return: None
        """
        await self.__update(User, class_id=user_id, available=available)

    async def group_post_id(self, group_id: int, new_post_id: int):
        """
        :param group_id: int
        :param new_post_id: int
        :return: None
        """
        await self.__update(Group, class_id=group_id, last_post_id=new_post_id)

    async def group_serviceable(self, group_id: int, serviceable: bool):
        """
        :param group_id: int
        :param serviceable: bool
        :return: None
        """
        await self.__update(Group, class_id=group_id, serviceable=serviceable)

    async def answer_nickname(self, answer_id: int, new_nickname: str):
        """
        :param answer_id: int
        :param new_nickname: str
        :return: None
        """
        await self.__update(Answer, class_id=answer_id, nickname=new_nickname)

    async def answer_message(self, answer_id: int, new_message: str):
        """
        :param answer_id: int
        :param new_message: str
        :return: None
        """
        await self.__update(Answer, class_id=answer_id, message=new_message)

    async def token_nickname(self, token_id: int, new_nickname: str):
        """
        :param token_id: int
        :param new_nickname:str
        :return: None
        """
        await self.__update(VkApiToken, class_id=token_id, nickname=new_nickname)

    async def token_serviceable(self, token_id: int, serviceable: str):
        """
        :param token_id: int
        :param serviceable: bool
        :return: None
        """
        await self.__update(VkApiToken, class_id=token_id, serviceable=serviceable)


updater = Updater()
