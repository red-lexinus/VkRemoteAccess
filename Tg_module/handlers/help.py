import asyncio
from aiogram import Dispatcher, types
from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import Text

from Tg_module.filters import ChatTypeFilter, InTextFilter
from Tg_module.keyboards import inline

cb_router = Router()


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_token'))
async def fun(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.answer('Заглушка( инфа зачем нужен токен)')
    await query.message.answer('Заглушка( инфа зачем нужен токен)')


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_get_token'))
async def fun(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.answer('Заглушка( инфа как получить токен)')
    await query.message.answer('Заглушка( инфа как получить токен)')


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_sub_group'))
async def fun(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.answer('Заглушка( инфа как подписаться на группу)')
    await query.message.answer('Заглушка( инфа как подписаться на группу)')


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_account'))
async def fun(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.answer('Заглушка( инфа как заданатить)')
    await query.message.answer('Заглушка( инфа как заданатить)')
