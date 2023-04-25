import asyncio
from aiogram.filters import Command
from aiogram import (Dispatcher, types, Router, F, flags)

import DbMager_module as Db

from Tg_module.filters import ChatTypeFilter
from Tg_module.keyboards import inline

router = Router()
router.message.filter(ChatTypeFilter('private'))


@router.message(F.text, Command('start'))
async def cmd_test(msg: types.Message) -> None:
    if Db.checker.user_exists_id(msg.from_user.id):
        await msg.answer('Вы уже зареганы')
    else:
        await msg.answer(f'Здравствуйте {msg.from_user.first_name} {msg.from_user.last_name}, '

                         f'данный бот поможет вам смотреть и комментировать посты из вк в своей '
                         f'телеге! Вам стоит использовать /help Чтобы понять как настроить бота')


@router.message(F.text, Command('help'))
async def cmd_test(msg: types.Message) -> None:
    await asyncio.sleep(10)
    await msg.answer(f'Всё хорошо, выбери, что хочешь знать',
                     reply_markup=inline.get_main_help_kb())


@router.message(F.text, Command('account'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Заглушка')


@router.message(F.text, Command('my_groups'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Заглушка')


@router.message(F.text, Command('my_tokens'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Заглушка')


@router.message(F.text, Command('setting_groups'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Заглушка')


@router.message(F.text, Command('setting_tokens'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer(f'Заглушка')


@router.message(F.text, Command('test'))
async def cmd_test(msg: types.Message) -> None:
    await msg.answer('Всё плохо брат, нет для тебя тестов, придётся самому учится')
