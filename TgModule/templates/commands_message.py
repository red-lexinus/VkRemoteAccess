def cmd_help() -> str:
    return 'Всё хорошо, выбери, что хочешь знать'


def cmd_account(user_name: str, tokens: int, subs: int, time_zone: int) -> str:
    if time_zone >= 0:
        time_zone = f'+{time_zone}'
    message = f"Здравствуйте {user_name}\nВаши возможности:\nКоличество акк: до {tokens}\n" \
              f"Количество групп: до {subs}\nВаше время UTF{time_zone}"
    return message


def cmd_start() -> str:
    return 'Зачем вам начинать сначала, может быть нужна помощь? /help'


def cmd_first_start(username: str) -> str:
    return f'Здравствуйте {username}, данный бот поможет вам смотреть и комментировать посты из вк ' \
           'в своей телеге! Вам стоит использовать /help Чтобы понять как настроить бота'


def cmd_test() -> str:
    return 'Всё плохо брат, нет для тебя тестов, придётся самому учится'


def user_no_groups() -> str:
    return "У вас нет подписок на какие-либо группы, /help вам в помощь"


def cmd_my_groups() -> str:
    return "Ваши группы"


def user_no_tokens() -> str:
    return "У вас пока нет токенов, /help вам в помощь"


def cmd_my_answers(count_answer: int) -> str:
    if count_answer:
        if count_answer == 1:
            return 'Хм вот ваши быстрые ответы, он 1'
        return f'Хм вот ваши быстрые ответы, их {count_answer}'
    return 'У вас нет быстрых ответов, поверьте это удобно, добавьте себе несколько!'
