from aiogram.types import inline_keyboard_button, inline_keyboard_markup
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from sqlalchemy.engine.row import Row as sqlalchemyRow

from DbManagerModule.DbClasses import Subscription, VkApiToken, Answer


class StandardAnswer(CallbackData, prefix="StA"):
    group_id: int
    post_id: int
    answer_id: int


class DetailedAnswer(CallbackData, prefix="DtA"):
    group_id: int
    post_id: int


class UserSubscription(CallbackData, prefix="USb"):
    group_id: int
    token_id: int | None
    action: str
    group_name: str | None


class UserToken(CallbackData, prefix="UTk"):
    token_id: int
    action: str


class UserAnswer(CallbackData, prefix="UAn"):
    answer_id: int
    action: str


class Commenting(CallbackData, prefix='Com'):
    action: str
    group_id: int
    post_id: int
    answer_id: int | None


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


def get_my_group_kb(groups: list[sqlalchemyRow[Subscription]]):
    builder = InlineKeyboardBuilder()
    for sub_data in groups:
        sub = sub_data[0]
        builder.button(text=f"{sub.nickname}",
                       callback_data=UserSubscription(group_id=sub.group_id, action="open").pack())
        builder.button(text="Отписаться", callback_data=UserSubscription(group_id=sub.group_id, action="del").pack())
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


def sub_new_group(group_id: int, group_name: str, tokens: list[VkApiToken]):
    builder = InlineKeyboardBuilder()
    for token in tokens:
        builder.button(
            text=f"Подписаться❤ {token.nickname}", callback_data=UserSubscription(
                group_id=group_id, token_id=token.id, action="sub", group_name=group_name).pack()
        )
    builder.adjust(1)
    return builder.as_markup()


def get_open_group_kb(group_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"Переименовать группу", callback_data=UserSubscription(
            group_id=group_id, action="rename").pack()
    )
    builder.adjust(1)
    return builder.as_markup()


def get_comment_post_ikb(group_id: int, post_id: int, answers: list[sqlalchemyRow[Answer]]):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f"написать ответ", callback_data=Commenting(action="deploy",
                                                         group_id=group_id, post_id=post_id, answer_id=None).pack()
    )
    for answer_data in answers:
        answer = list(answer_data)[0]
        builder.button(
            text=f"{answer.nickname}", callback_data=Commenting(action="send",
                                                                group_id=group_id, post_id=post_id,
                                                                answer_id=answer.id).pack()
        )
    builder.adjust(1, 2)
    return builder.as_markup()
