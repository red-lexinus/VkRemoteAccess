import asyncio

from aiogram import Router, F, Dispatcher, types
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from DbManagerModule import getter, creator, checker
from VkApiModule import vk_parser, ParseClasses
from TgModule.filters import ChatTypeFilter, InTextFilter
from TgModule.templates import commenting_message
from TgModule.keyboards import inline
from TgModule.fsm.base_fsm import DeployComment

cb_router = Router()
fms_router = Router()

cb_router.message.filter(ChatTypeFilter('private'))
fms_router.message.filter(ChatTypeFilter('private'))


@cb_router.callback_query(inline.Commenting.filter(F.action == 'send'))
async def send_standard_comment(query: CallbackQuery, callback_data: inline.Commenting) -> None:
    comment_data = await getter.answer(callback_data.answer_id)
    token_data = await getter.token_by_sub(query.from_user.id, callback_data.group_id)
    if token_data and comment_data:
        token, comment = token_data.token, comment_data.message
        data = ParseClasses.VkParserCommentPost(
            token=token, group_id=callback_data.group_id, post_id=callback_data.post_id, comment=comment
        )
        res = await vk_parser.new_comment(data)
        if res:
            await query.message.answer(commenting_message.success_commenting())
        else:
            await query.message.answer(commenting_message.error_commenting())
    else:
        await query.message.answer(commenting_message.error_lack_data())
    await query.answer()


@cb_router.callback_query(inline.Commenting.filter(F.action == 'deploy'))
async def deploy_comment(query: CallbackQuery, callback_data: inline.Commenting, state: FSMContext) -> None:
    token_data = await getter.token_by_sub(query.from_user.id, callback_data.group_id)
    if token_data:
        await state.set_state(DeployComment.post_id)
        await state.update_data(token=token_data.token, group_id=callback_data.group_id, post_id=callback_data.post_id)
        await query.message.answer(commenting_message.input_command())
        await query.answer()
    else:
        await query.message.answer(commenting_message.error_lack_data())
        await query.answer()


@fms_router.message(DeployComment.post_id, F.text)
async def set_new_time_zone(msg: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    data = ParseClasses.VkParserCommentPost(
        token=state_data['token'], group_id=state_data['group_id'], post_id=state_data['post_id'], comment=msg.text
    )
    res = await vk_parser.new_comment(data)
    if res:
        await msg.answer(commenting_message.success_commenting())
    else:
        await msg.answer(commenting_message.error_commenting())
    await state.clear()
