import asyncio
from aiogram.filters import Command
from aiogram import Dispatcher, types
from aiogram import Router
from aiogram import F

from Tg_module.filters import ChatTypeFilter

router = Router()


@router.message(F.text, ChatTypeFilter('private'), Command('start'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Здравствуйте {msg.from_user.username}, данный бот поможет вам смотреть,'
                     f' комментировать посты из вк в своей телеге!')


@router.message(F.text, ChatTypeFilter('private'), Command('help'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Здравствуйте {msg.from_user.username}, данный бот поможет вам смотреть,'
                     f' комментировать посты из вк в своей телеге!')


@router.message(F.text, ChatTypeFilter('private'), Command('account'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Ваш аккаунт Стандартный, нет никаких купленных дополнений')


@router.message(F.text, ChatTypeFilter('private'), Command('my_groups'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer('Ваши группы')


@router.message(F.text, ChatTypeFilter('private'), Command('my_tokens'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer('Ваши токены')


@router.message(F.text, ChatTypeFilter('private'), Command('setting_groups'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer('Настройка групп')


@router.message(F.text, ChatTypeFilter('private'), Command('setting_tokens'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer('Настройка токенов')


@router.message(F.text, ChatTypeFilter('private'), Command('test'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer('Всё плохо брат, нет для тебя тестов, придётся самому учится')
