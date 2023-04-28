from aiogram.fsm.state import State, StatesGroup


class DetailedAnswer(StatesGroup):
    group_id = State()
    post_id = State()


class RenameToken(StatesGroup):
    token_id = State()
    token_name = State()


class RenameGroup(StatesGroup):
    group_id = State()
    group_name = State()


class ChangeTimeZone(StatesGroup):
    time_zone = State()


class ChangeAnswer(StatesGroup):
    answer_id = State()
    answer = State()
    nickname = State()


class CreateAnswer(StatesGroup):
    answer = State()
    nickname = State()
