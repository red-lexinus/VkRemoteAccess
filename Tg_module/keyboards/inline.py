from aiogram.types import inline_keyboard_button, inline_keyboard_markup
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from sqlalchemy.engine.row import Row as sqlalchemyRow

from DbManagerModule.DbClasses import Group, VkApiToken, Answer


class StandardAnswer(CallbackData, prefix="StA"):
    group_id: int
    post_id: int
    answer_id: int


class DetailedAnswer(CallbackData, prefix="DtA"):
    group_id: int
    post_id: int


class UserSubscription(CallbackData, prefix="USb"):
    group_id: int
    action: str


class UserToken(CallbackData, prefix="UTk"):
    token_id: int
    action: str


class UserAnswer(CallbackData, prefix="UAn"):
    answer_id: int
    action: str


class MainDialog(CallbackData, prefix="MnD"):
    next_dialog: str


# callback_data=StandardAnswer(group_id=1, post_id=2, answer_id=3).pack()

def get_main_help_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Зачем нужен token",
        callback_data=MainDialog(next_dialog='help_token').pack())
    builder.button(
        text="Как и где получить token",
        callback_data=MainDialog(next_dialog='help_get_token').pack())
    builder.button(
        text="Как добавить группу или токен",
        callback_data=MainDialog(next_dialog='help_add_sub&token').pack())
    builder.button(
        text="Как расширить свои возможности",
        callback_data=MainDialog(next_dialog='help_account').pack())
    builder.adjust(1)
    return builder.as_markup()


def get_help_account_kb():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Увеличить возможности",
        callback_data=MainDialog(next_dialog='donate_start_menu').pack())
    builder.button(
        text="Изменить время",
        callback_data=MainDialog(next_dialog='change_time_zone').pack())
    builder.adjust(1)
    return builder.as_markup()


def get_answer():
    builder = InlineKeyboardBuilder()
    builder.button(text="Тест", callback_data=StandardAnswer(group_id=1, post_id=2, answer_id=3).pack())
    return builder.as_markup()


def get_my_group_kb(groups: list[sqlalchemyRow[Group, int]]):
    builder = InlineKeyboardBuilder()
    for sub in groups:
        s = list(sub)
        group_id, group_name = s[0].id, s[1]
        builder.button(text=f"{group_name}", callback_data=UserSubscription(group_id=group_id, action="open").pack())
        builder.button(text="Отписаться", callback_data=UserSubscription(group_id=group_id, action="del").pack())
    builder.adjust(2)
    return builder.as_markup()


def get_my_tokens_kb(tokens: list[sqlalchemyRow[VkApiToken]]):
    builder = InlineKeyboardBuilder()
    for token_data in tokens:
        token = list(token_data)[0]
        builder.button(text=f"{token.nickname}", callback_data=UserToken(token_id=token.id, action="open").pack())
        builder.button(text="Удалить", callback_data=UserToken(token_id=token.id, action="del").pack())
    builder.adjust(2)
    return builder.as_markup()


def get_my_answers_kb(answers: list[sqlalchemyRow[Answer]]):
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить новый быстрый ответ", callback_data=MainDialog(next_dialog='new_answer'))
    for answer_data in answers:
        answer = list(answer_data)[0]
        builder.button(text=f"{answer.nickname}", callback_data=UserAnswer(answer_id=answer.id, action="open").pack())
        builder.button(text="Удалить", callback_data=UserAnswer(answer_id=answer.id, action="del").pack())
    builder.adjust(1, 2)
    return builder.as_markup()


def get_open_answer(answer_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить текст ответа", callback_data=UserAnswer(answer_id=answer_id, action="chg_ans").pack())
    builder.button(text="Изменить сокращение", callback_data=UserAnswer(answer_id=answer_id, action="chg_nik").pack())
    builder.button(text="Удалить авто-ответ", callback_data=UserAnswer(answer_id=answer_id, action="del").pack())
    builder.adjust(1)
    return builder.as_markup()
