from aiogram.types import inline_keyboard_button, inline_keyboard_markup
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class StandardAnswer(CallbackData, prefix="StA"):
    group_id: int
    post_id: int
    answer_id: int


class DetailedAnswer(CallbackData, prefix="DtA"):
    group_id: int
    post_id: int


class MainDialog(CallbackData, prefix="MnD"):
    next_dialog: str


# callback_data=StandardAnswer(group_id=1, post_id=2, answer_id=3).pack()

def get_main_help_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Зачем нужен token",
        callback_data=MainDialog(next_dialog='help_token').pack())
    builder.button(
        text=f"Как и где получить token",
        callback_data=MainDialog(next_dialog='help_get_token').pack())
    builder.button(
        text=f"Как подписаться на вк группу",
        callback_data=MainDialog(next_dialog='help_sub_group').pack())
    builder.button(
        text=f"Как расширить свои возможности",
        callback_data=MainDialog(next_dialog='help_account').pack())
    builder.adjust(1)
    return builder.as_markup()


def get_answer():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Тест", callback_data=StandardAnswer(group_id=1, post_id=2, answer_id=3).pack())
    return builder.as_markup()
