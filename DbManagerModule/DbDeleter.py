from sqlalchemy import delete

from .DbClasses import Base, User, Group, Answer, VkApiToken, Subscription
from .DbCore import core


class Deleter:
    def __init__(self):
        self.__async_session = core.get_new_async_session()

    async def __del_db_classes(self, db_class: Base, class_id: int):
        obj = delete(db_class).filter_by(id=class_id)
        await self.__async_session.execute(obj)
        await self.__async_session.commit()

    async def __del_list_db_classes(self, db_class: Base, **kwargs):
        obj = delete(db_class).filter_by(**kwargs)
        await self.__async_session.execute(obj)
        await self.__async_session.commit()

    async def __check_kwargs(self, **kwargs):
        pass

    async def users_filter(self, **kwargs):
        """
        :param kwargs:
            'id'(user_id): type:int
            'available': type:bool
            'time_zone': type:int
        :return: None
        """
        await self.__check_kwargs(**kwargs)
        await self.__del_list_db_classes(User, **kwargs)

    async def groups_filter(self, **kwargs) -> None:
        """
        :param kwargs:
            'id'(group_id): type:int
            'domain': type:str
            'serviceable': type:bool
            'last_post_id': type:int
        :return: None
        """
        await self.__check_kwargs(**kwargs)
        await self.__del_list_db_classes(Group, **kwargs)

    async def answers_filter(self, **kwargs) -> None:
        """
        :param kwargs:
            'id'(answer_id): type:int
            'user_id': type:int
            'message': type:str
            'nickname': type:str
        :return: None
        """
        await self.__check_kwargs(**kwargs)
        await self.__del_list_db_classes(Answer, **kwargs)

    async def tokens_filter(self, **kwargs) -> None:
        """
        :param kwargs:
            'id'(token_id): type:int
            'user_id': type:int
            'token': type:str
            'nickname': type:str
            'serviceable': type:bool
        :return: None
        """
        await self.__check_kwargs(**kwargs)
        await self.__del_list_db_classes(VkApiToken, **kwargs)

    async def subs_filter(self, **kwargs) -> None:
        """
        :param kwargs:
            'id'(subscription_id): type:int
            'user_id': type:int
            'group_id': type:int
            'token_id': type:int
        :return: None
        """
        await self.__check_kwargs(**kwargs)
        await self.__del_list_db_classes(Subscription, **kwargs)

    async def user(self, user_id: int) -> None:
        """
        :param user_id: int
        :return: None
        """
        await self.__del_db_classes(User, user_id)

    async def answer(self, answer_id: int) -> None:
        """
        :param answer_id: int
        :return: None
        """
        await self.__del_db_classes(Answer, answer_id)

    async def group(self, group_id: int) -> None:
        """
        :param group_id: int
        :return: None
        """
        await self.__del_db_classes(Group, group_id)

    async def token(self, token_id: int) -> None:
        """
        :param token_id: int
        :return: None
        """
        await self.__del_db_classes(VkApiToken, token_id)

    async def sub(self, sub_id: int) -> None:
        """
        :param sub_id: int
        :return: None
        """
        await self.__del_db_classes(Subscription, sub_id)


deleter = Deleter()
