from sqlalchemy import select, join

from .DbClasses import Base, User, Group, Answer, VkApiToken, Subscription, UserRights
from .DbCore import core


class Getter:
    def __init__(self):
        self.__async_session = core.get_async_session()

    async def __check_kwargs(self, **kwargs):
        pass

    async def __return_list_db_classes(self, db_class: Base, **kwargs) -> list[Base]:
        data = await self.__async_session.execute(
            select(db_class).filter_by(**kwargs)
        )
        return data.fetchall()

    async def __return_db_classes(self, db_class: Base, class_id: int) -> Base | None:
        data = await self.__async_session.scalars(
            select(db_class).filter_by(id=class_id)
        )
        res = data.fetchall()
        if res:
            return res[0]
        return None

    async def users_filter(self, **kwargs) -> list[User]:
        """
        :param kwargs:
            'id'(user_id): type:int
            'available': type:bool
            'time_zone': type:int
        :rtype: list[DbClasses.User]
        :return: list[DbClasses.User]
        """
        await self.__check_kwargs(**kwargs)
        return await self.__return_list_db_classes(User, **kwargs)

    async def user_rights_filter(self, **kwargs) -> list[UserRights]:
        """
        :param kwargs:
            'user_id': type:int
            'max_tokens': type:int
            'max_subs': type:int
            'donate': type:bool
        :rtype: list[DbClasses.UserRights]
        :return: list[DbClasses.UserRights]
        """
        await self.__check_kwargs(**kwargs)
        return await self.__return_list_db_classes(UserRights, **kwargs)

    async def groups_filter(self, **kwargs) -> list[Group]:
        """
        :param kwargs:
            'id'(group_id): type:int
            'domain': type:str
            'serviceable': type:bool
            'last_post_id': type:int
        :rtype: list[DbClasses.Group]
        :return: list[DbClasses.Group]
        """
        await self.__check_kwargs(**kwargs)
        return await self.__return_list_db_classes(Group, **kwargs)

    async def answers_filter(self, **kwargs) -> list[Answer]:
        """
        :param kwargs:
            'id'(answer_id): type:int
            'user_id': type:int
            'message': type:str
            'nickname': type:str
        :rtype: list[DbClasses.Answer]
        :return: list[DbClasses.Answer]
        """
        await self.__check_kwargs(**kwargs)
        return await self.__return_list_db_classes(Answer, **kwargs)

    async def tokens_filter(self, **kwargs) -> list[VkApiToken]:
        """
        :param kwargs:
            'id'(token_id): type:int
            'user_id': type:int
            'token': type:str
            'nickname': type:str
            'serviceable': type:bool
        :rtype: list[DbClasses.VkApiToken]
        :return: list[DbClasses.VkApiToken]
        """
        await self.__check_kwargs(**kwargs)
        return await self.__return_list_db_classes(VkApiToken, **kwargs)

    async def subs_filter(self, **kwargs) -> list[Subscription]:
        """
        :param kwargs:
            'id'(subscription_id): type:int
            'user_id': type:int
            'group_id': type:int
            'token_id': type:int
        :rtype: list[DbClasses.Subscription]
        :return: list[DbClasses.Subscription]
        """
        await self.__check_kwargs(**kwargs)
        return await self.__return_list_db_classes(Subscription, **kwargs)

    async def user(self, user_id: int) -> User:
        """
        :param user_id: int
        :rtype: DbClasses.User
        :return: DbClasses.User
        """
        return await self.__return_db_classes(User, user_id)

    async def user_rights(self, user_id: int) -> UserRights:
        """
        :param user_id: int
        :rtype: DbClasses.UserRights
        :return: DbClasses.UserRights
        """
        return await self.__return_db_classes(UserRights, user_id)

    async def group(self, group_id: int) -> Group:
        """
        :param group_id: int
        :rtype: DbClasses.Group
        :return: DbClasses.Group
        """
        return await self.__return_db_classes(Group, group_id)

    async def token(self, token_id: int) -> VkApiToken:
        """
        :param token_id: int
        :rtype: DbClasses.VkApiToken
        :return: DbClasses.VkApiToken
        """
        return await self.__return_db_classes(VkApiToken, token_id)

    async def sub(self, sub_id: int) -> Subscription:
        """
        :param sub_id: int
        :rtype: DbClasses.Subscription
        :return: DbClasses.Subscription
        """
        return await self.__return_db_classes(Subscription, sub_id)

    async def answer(self, answer_id: int) -> Answer:
        """
        :param answer_id: int
        :rtype: DbClasses.Answer
        :return: DbClasses.Answer
        """
        return await self.__return_db_classes(Answer, answer_id)

    async def user_all_subs(self, user_id: int) -> list:
        """
        :param user_id: int
        :return:
        """
        data = await self.__async_session.execute(
            select(Group, Subscription.nickname).join(Subscription).filter_by(user_id=user_id))
        return data.fetchall()


getter = Getter()

