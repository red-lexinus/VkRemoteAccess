import asyncio
from aiogram import Dispatcher, types
from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import Text

import DbMager_module as Db

from Tg_module.filters import ChatTypeFilter, InTextFilter
from Tg_module.keyboards import inline

router = Router()
router.message.filter(ChatTypeFilter('private'))


@router.message(F.text)
async def unknown_handler(msg: types.Message) -> None:
    await msg.reply('Проверка')


@router.callback_query(inline.StandardAnswer.filter(F.group_id == 1))
async def fun(query: CallbackQuery, callback_data: inline.StandardAnswer):
    pass

# @router.message(F.text, InTextFilter('*'))
# async def vk_url_handler(msg: types.Message) -> None:
#     await msg.reply(f'Тут {msg.text.count("*")} звёздочек')
#
#
# def fun():
#     return F.forward_from_chat[F.type == "channel"].as_("channel")
#
#
# @router.message(fun())
# async def forwarded_from_channel(message: types.Message, channel: types.Chat):
#     await message.answer(f"This channel's ID is {channel.id}")
