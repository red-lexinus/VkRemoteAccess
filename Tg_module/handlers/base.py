import asyncio
from aiogram import Dispatcher, types
from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import Text

from Tg_module.filters import ChatTypeFilter, InTextFilter
from Tg_module.keyboards import inline

router = Router()


# @router.message(F.text, InTextFilter('*'))
# async def vk_url_handler(msg: types.Message) -> None:
#     await msg.reply(f'Тут {msg.text.count("*")} звёздочек')
#
#
@router.message(F.text, ChatTypeFilter('private'))
async def unknown_handler(msg: types.Message) -> None:
    await msg.reply('Проверка', reply_markup=inline.get_answer())


@router.callback_query(inline.StandardAnswer.filter(F.group_id == 1))
async def fun(query: CallbackQuery, callback_data: inline.StandardAnswer):
    pass
