def change_time_zone() -> str:
    return 'Напишите ваше время, доступные форматы: UTF+3 или 3'


def set_new_time_zone(new_time_zone: int) -> str:
    if new_time_zone >= 0:
        new_time_zone = f'+{new_time_zone}'
    return f'Вам поменяли время! ваше текущее время: UTF{new_time_zone}'


def error_set_new_time_zone() -> str:
    return 'Вы ввели своё время не в том формате, попробуйте снова! Доступные форматы: UTF+3 или 3'


def new_answer() -> str:
    return 'Всё просто, сначала вам нужно написать сам ответ, дождаться ответа бота, а после написать ' \
           'узнаваемое сокращение, которое будет предлагать вам бот, всё для последующего удобства'


def open_answer(nickname: str, answer: str) -> str:
    return f'{nickname}:\n{answer}'


def fsm_create_answer_msg() -> str:
    return 'Вот, а теперь напишите сокращение, которое будет предлагать вам бот'


def fsm_create_answer_nk() -> str:
    return 'Вот! автоматический ответ сохранён, теперь наслаждайтесь жизнью'


def del_answer() -> str:
    return "Вы успешно удалили быстрый ответ"


def change_answer() -> str:
    return "Просто напишите новый текст ответа!"


def change_answer_nickname() -> str:
    return "Просто напишите новое сокращение ответа!"


def fsm_change_answer() -> str:
    return "Вы успешно изменили текст ответа"


def fsm_change_answer_nickname() -> str:
    return "Вы успешно изменили сокращённое имя ответа"
