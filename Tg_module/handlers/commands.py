import asyncio
from aiogram.filters import Command
from aiogram import (Dispatcher, types, Router, F, flags)
from aiogram.fsm.context import FSMContext

from DbManagerModule import checker, getter, creator
from Tg_module.filters import ChatTypeFilter
from Tg_module.keyboards import inline
from Tg_module.templates import commands_message

router = Router()
router.message.filter(ChatTypeFilter('private'))


@router.message(F.text, Command('start'))
async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    if await checker.user_exists(id=msg.from_user.id):
        await msg.answer(commands_message.cmd_start())
    else:
        await creator.new_user(msg.from_user.id)
        await msg.answer(commands_message.cmd_first_start(msg.from_user.username))


@router.message(F.text, Command('help'))
async def cmd_help(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(commands_message.cmd_help(),
                     reply_markup=inline.get_main_help_kb())


@router.message(F.text, Command('account'))
async def cmd_account(msg: types.Message, state: FSMContext) -> None:
    if not await checker.user_exists(id=msg.from_user.id):
        creator.new_user(msg.from_user.id)
    user_data = await getter.user(msg.from_user.id)
    user_rights = await getter.user_rights(msg.from_user.id)
    message = commands_message.cmd_account(
        msg.from_user.username, user_rights.max_tokens, user_rights.max_subs, user_data.time_zone
    )
    await msg.answer(message, reply_markup=inline.get_help_account_kb())


@router.message(F.text, Command('my_groups'))
async def cmd_my_groups(msg: types.Message, state: FSMContext) -> None:
    groups = await getter.user_all_subs(msg.from_user.id)
    if groups:
        ikb = inline.get_my_group_kb(groups)
        await msg.answer(commands_message.cmd_my_groups(), reply_markup=ikb)
    else:
        await msg.answer(commands_message.user_no_groups())


@router.message(F.text, Command('my_tokens'))
async def cmd_my_tokens(msg: types.Message, state: FSMContext) -> None:
    tokens = await getter.tokens_filter(user_id=msg.from_user.id)
    if tokens:
        ikb = inline.get_my_tokens_kb(tokens)
        await msg.answer(commands_message.cmd_my_groups(), reply_markup=ikb)
    else:
        await msg.answer(commands_message.user_no_tokens())


@router.message(F.text, Command('my_answers'))
async def cmd_my_answers(msg: types.Message, state: FSMContext) -> None:
    answers = await getter.answers_filter(user_id=msg.from_user.id)
    ikb = inline.get_my_answers_kb(answers)
    await msg.answer(commands_message.cmd_my_answers(len(answers)), reply_markup=ikb)


@router.message(F.text, Command('test'))
async def cmd_test(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(commands_message.cmd_test())
