import asyncio
from aiogram import (F, Router, Bot, types)
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMedia
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from TgModule.filters import ChatTypeFilter, InTextFilter
from TgModule.fsm import base_fsm
from TgModule.keyboards import inline
from TgModule.templates import setting_message
from DbManagerModule import updater, creator, getter, deleter, checker
from VkApiModule import vk_parser, ParseClasses

cb_router = Router()
fms_router = Router()

cb_router.message.filter(ChatTypeFilter('private'))
fms_router.message.filter(ChatTypeFilter('private'))


@cb_router.callback_query(inline.UserSubscription.filter(F.action == 'rename'))
async def open_sub(query: CallbackQuery, callback_data: inline.UserSubscription, state: FSMContext):
    # await query.answer(f'Заглушка {callback_data.action}')
    await state.set_state(base_fsm.RenameGroup.group_id)
    await state.update_data(group_id=callback_data.group_id)
    await query.message.answer(setting_message.rename_group())
    await query.answer()


@cb_router.callback_query(inline.UserSubscription.filter(F.action == 'open'))
async def open_sub(query: CallbackQuery, callback_data: inline.UserSubscription):
    groups = await getter.subs_filter(group_id=callback_data.group_id, user_id=query.from_user.id)
    if groups:
        group = groups[0][0]
        token = await getter.token(group.token_id)
        data = await vk_parser.get_group_info(
            ParseClasses.VkParserGroupId(token=token.token, group_id=group.group_id)
        )
        await query.message.answer_photo(
            photo=data.photo_200, caption=setting_message.open_group(group.nickname),
            reply_markup=inline.get_open_group_kb(callback_data.group_id)
        )
    else:
        await query.message.answer(setting_message.none_sub_group())
    await query.answer()


@cb_router.callback_query(inline.UserSubscription.filter(F.action == 'del'))
async def dell_sub(query: CallbackQuery, callback_data: inline.UserSubscription):
    await deleter.subs_filter(group_id=callback_data.group_id, user_id=query.from_user.id)
    await query.message.answer(setting_message.success_del_sub())
    await query.answer()


@cb_router.callback_query(inline.UserSubscription.filter(F.action == 'sub'))
async def change_time_zone(query: CallbackQuery, callback_data: inline.UserSubscription):
    if await checker.new_sub(query.from_user.id):
        await creator.new_subs(
            callback_data.group_id, query.from_user.id, callback_data.token_id, callback_data.group_name
        )
        if not await checker.group_exists(id=callback_data.group_id):
            token = await getter.token(callback_data.token_id)
            parse_data = ParseClasses.VkParserGroupId(
                token=token.token, group_id=callback_data.group_id
            )
            group_data = await vk_parser.get_group_info(parse_data)
            last_post_id = await vk_parser.get_group_last_post_id(parse_data)
            await creator.new_group(group_data.id, group_data.screen_name, last_post_id.id)
        await query.message.answer(setting_message.success_sub())
    else:
        await query.message.answer(setting_message.max_subs())
    await query.answer()
    # print(await bot.answer_callback_query(query.id, 'Проверка чувааак'))


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'change_time_zone'))
async def change_time_zone(query: CallbackQuery, state: FSMContext):
    await state.set_state(base_fsm.ChangeTimeZone.time_zone)
    await query.message.answer(setting_message.change_time_zone())
    await query.answer()


@cb_router.callback_query(inline.MainDialog.filter(F.next_dialog == 'new_answer'))
async def new_answer(query: CallbackQuery, state: FSMContext):
    await state.set_state(base_fsm.CreateAnswer.answer)
    await query.message.answer(setting_message.new_answer())
    await query.answer()


@cb_router.callback_query(inline.UserAnswer.filter(F.action == 'open'))
async def open_answer(query: CallbackQuery, callback_data: inline.UserAnswer, state: FSMContext):
    answer_data = await getter.answer(callback_data.answer_id)
    ikb = inline.get_open_answer(answer_data.id)
    await query.message.answer(setting_message.open_answer(answer_data.nickname, answer_data.message), reply_markup=ikb)
    await query.answer()


@cb_router.callback_query(inline.UserAnswer.filter(F.action == 'chg_ans'))
async def change_answer(query: CallbackQuery, callback_data: inline.UserAnswer, state: FSMContext):
    answer_data = await getter.answer(callback_data.answer_id)
    await state.set_state(base_fsm.ChangeAnswer.answer)
    await state.update_data(answer_id=answer_data.id)
    await query.message.answer(setting_message.change_answer())
    await query.answer()


@cb_router.callback_query(inline.UserAnswer.filter(F.action == 'chg_nik'))
async def change_answer_nickname(query: CallbackQuery, callback_data: inline.UserAnswer, state: FSMContext):
    answer_data = await getter.answer(callback_data.answer_id)
    await state.set_state(base_fsm.ChangeAnswer.nickname)
    await state.update_data(answer_id=answer_data.id)
    await query.message.answer(setting_message.change_answer_nickname())
    await query.answer()


@cb_router.callback_query(inline.UserAnswer.filter(F.action == 'del'))
async def del_answer(query: CallbackQuery, callback_data: inline.UserAnswer, state: FSMContext):
    answer_data = await getter.answer(callback_data.answer_id)
    await deleter.answer(answer_data.id)
    await query.message.answer(setting_message.del_answer())
    await query.answer()


@fms_router.message(base_fsm.CreateAnswer.answer, F.text)
async def fsm_create_answer_msg(msg: types.Message, state: FSMContext) -> None:
    await state.update_data(answer=msg.text)
    await state.set_state(base_fsm.CreateAnswer.nickname)
    await msg.reply(setting_message.fsm_create_answer_msg())


@fms_router.message(base_fsm.CreateAnswer.nickname, F.text)
async def fsm_create_answer_nk(msg: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await creator.new_answer(msg.from_user.id, data['answer'], msg.text)
    await msg.reply(setting_message.fsm_create_answer_nk())


@fms_router.message(base_fsm.ChangeAnswer.answer, F.text)
async def fsm_change_answer(msg: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await updater.answer_message(data['answer_id'], msg.text)
    await msg.reply(setting_message.fsm_change_answer())


@fms_router.message(base_fsm.ChangeAnswer.nickname, F.text)
async def fsm_change_answer_nickname(msg: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await updater.answer_nickname(data['answer_id'], msg.text)
    await msg.reply(setting_message.fsm_change_answer_nickname())


@fms_router.message(base_fsm.ChangeTimeZone.time_zone, F.text)
async def set_new_time_zone(msg: types.Message, state: FSMContext) -> None:
    new_time_zone = parse_time_msg(msg.text)
    if type(new_time_zone) == int:
        await updater.user_time_zone(msg.from_user.id, new_time_zone)
        await msg.answer(setting_message.set_new_time_zone(new_time_zone))
        await state.clear()
    else:
        await msg.answer(setting_message.error_set_new_time_zone())


@fms_router.message(base_fsm.RenameGroup.group_id, F.text)
async def set_new_group_name(msg: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    group_id = data['group_id']
    await updater.sub_nickname(user_id=msg.from_user.id, group_id=group_id, nickname=msg.text)
    await msg.answer(setting_message.success_rename_group(new_nickname=msg.text))
    await state.clear()


def parse_time_msg(msg: str) -> int | None:
    msg.upper()
    try:
        if 'UTF' in msg:
            msg = msg.split('UTF')[1]
        return int(msg)
    except ValueError:
        return None
