import asyncio
from aiogram import Dispatcher, types
from aiogram import Router
from aiogram import F

from aiogram.filters import Text

from Tg_module.filters import ChatTypeFilter, InTextFilter

router = Router()




# @router.message(F.text, InTextFilter('*'))
# async def vk_url_handler(msg: types.Message) -> None:
#     await msg.reply(f'Тут {msg.text.count("*")} звёздочек')
#
#
# @router.message(F.text, ChatTypeFilter('private'))
# async def unknown_handler(msg: types.Message) -> None:
#     await msg.reply(msg.chat.type)
