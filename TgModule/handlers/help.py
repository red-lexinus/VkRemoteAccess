from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery

from TgModule.filters import ChatTypeFilter
from TgModule.templates import help_message
from TgModule.keyboards import inline

cb_router = Router()
cb_router.message.filter(ChatTypeFilter('private'))


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_token'))
async def help_token(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.message.answer('Заглушка( инфа зачем нужен токен)')
    await query.answer()


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_get_token'))
async def help_get_token(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.message.answer('Заглушка( инфа как получить токен)')
    await query.answer()


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_add_sub&token'))
async def help_add_sub_token(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.message.answer(help_message.help_add_sub_token())
    await query.answer()


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'help_account'))
async def help_account(query: CallbackQuery, callback_data: inline.MainDialog):
    await query.message.answer('Заглушка( инфа как заданатить)')
    await query.answer()
