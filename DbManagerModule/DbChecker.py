from sqlalchemy import select

from DbManagerModule.DbCore import core
from DbManagerModule.DbClasses import (User, Group, Answer, VkApiToken, Subscription, UserRights, Base)


class Checker:
    def __init__(self):
        self.__async_session = core.get_async_session()

    async def __check(self, dm_class: Base, **kwargs) -> bool:
        obj = await self.__async_session.scalars(
            select(dm_class.id).filter_by(**kwargs)
        )
        if obj.fetchall():
            return True
        return False

    async def __check_kwargs(self, **kwargs):
        pass

    async def user_exists(self, **kwargs) -> bool:
        """
        :param kwargs:
            'id'(user_id): type:int
            'available': type:bool
            'time_zone': type:int
        :rtype: bool
        :return: Ответ, существует ли такой user в бд
        Пример:
        kwargs = {
            'id' = 1,
            'available' = True
        }
        if await Checker().user_exists(**kwargs):
            print('Да!! Пользователь существует и доступен!')
        else:
            print('Всё не так!')
        """
        await self.__check_kwargs(**kwargs)
        return await self.__check(User, **kwargs)

    async def group_exists(self, **kwargs) -> bool:
        """
        :param kwargs:
            'id'(group_id): type:int
            'domain': type:str
            'serviceable': type:bool
            'last_post_id': type:int
        :rtype: bool
        :return: Ответ, существует ли такой group в бд
        Пример:
        kwargs = {
            'id' = 1,
            'serviceable' = True
        }
        if await Checker().group_exists(**kwargs):
            print('Да!! Группа существует и доступна!')
        else:
            print('Всё не так!')
        """
        await self.__check_kwargs(**kwargs)
        return await self.__check(Group, **kwargs)

    async def answer_exists(self, **kwargs) -> bool:
        """
        :param kwargs:
            'id'(answer_id): type:int
            'user_id': type:int
            'message': type:str
            'nickname': type:str
        :rtype: bool
        :return: Ответ, существует ли такой answer в бд
        Пример:
        kwargs = {
            'user_id': 1,
            'message': 'сообщение'
        }
        if await Checker().answer_exists(**kwargs):
            print(f'У пользователя(user_id={kwargs["user_id"]}) есть ответ с текстом: {kwargs["message"]}')
        else:
            print('Всё не так!')
        """
        await self.__check_kwargs(**kwargs)
        return await self.__check(Answer, **kwargs)

    async def sub_exists(self, **kwargs) -> bool:
        """
        :param kwargs:
            'id'(subscription_id): type:int
            'user_id': type:int
            'group_id': type:int
            'token_id': type:int
        :rtype: bool
        :return: Ответ, существует ли такой subscription в бд
        Пример:
        kwargs = {
            'user_id' = 1,
            'group_id' = 1
        }
        if await Checker().sub_exists(**kwargs):
            print(f'Пользователь(user_id={kwargs["user_id"]}) подписан на группу(group_id={kwargs["group_id"]})')
        else:
            print('Всё не так!')
        """
        await self.__check_kwargs(**kwargs)
        return await self.__check(Subscription, **kwargs)

    async def token_exists(self, **kwargs) -> bool:
        """
        :param kwargs:
            'id'(token_id): type:int
            'user_id': type:int
            'token': type:str
            'nickname': type:str
            'serviceable': type:bool
        :rtype: bool
        :return: Ответ, существует ли такой token в бд
        Пример:
        kwargs = {
            'user_id': 1,
            'serviceable': True
        }
        if await Checker().token_exists(**kwargs):
            print(f'У пользователя(user_id={kwargs["user_id"]}) есть рабочий token')
        else:
            print('Всё не так!')
        """
        await self.__check_kwargs(**kwargs)
        return await self.__check(VkApiToken, **kwargs)

    async def new_sub(self, user_id: int) -> bool:
        """
        :param user_id: type:int
        :rtype: bool
        :return: Ответ, можно ли пользователю добавить подписку на группу
        """
        user_root = await self.__async_session.execute(
            select(UserRights).filter_by(id=user_id)
        )
        user_subs = await self.__async_session.execute(
            select(Subscription.id).filter_by(user_id=user_id)
        )
        return user_root.fetchall()[0][0].max_subs > len(user_subs.fetchall())


checker = Checker()
