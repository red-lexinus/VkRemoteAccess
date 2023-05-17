from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder
from aiogram.types import KeyboardButton


def __create_main_kb():
    builder = ReplyKeyboardBuilder()
    buttons_data = ['текст_1', 'текст_2']
    for txt in buttons_data:
        builder.add(KeyboardButton(text=txt))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


main_kb = __create_main_kb()
