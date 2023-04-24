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


# callback_data=StandardAnswer(group_id=1, post_id=2, answer_id=3).pack()
def get_answer():
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Тест", callback_data=StandardAnswer(group_id=1, post_id=2, answer_id=3).pack())
    return builder.as_markup()
