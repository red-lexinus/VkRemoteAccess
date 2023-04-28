import asyncio
from aiogram import Dispatcher, types
from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.filters import Text

from Tg_module.filters import ChatTypeFilter, InTextFilter
from Tg_module.templates import base_message
from Tg_module.keyboards import inline

router = Router()
router.message.filter(ChatTypeFilter('private'))


@router.message(F.text, InTextFilter('vk1.a.'))
async def new_group_handler(msg: types.Message) -> None:
    await msg.reply('Затычка')


@router.message(F.text, InTextFilter('vk.com'))
async def new_group_handler(msg: types.Message) -> None:
    await msg.reply('Затычка')


@router.message(F.text)
async def unknown_handler(msg: types.Message) -> None:
    await msg.reply(base_message.unknown_handler(msg.text))
