def success_commenting():
    return "Вы успешно оставили комментарий"


def error_commenting():
    return 'Не удалось оставить комментарий'


def error_lack_data():
    return 'Не найдены некоторые необходимые данные для отправки комментария\nВозможные причины:\n1) Удалили токен вк' \
           '\n2) Отписались от паблика\n3) Удалили быстрый ответ, который сейчас использовали(если использовали)'


def input_command():
    return 'Напишите ваш комментарий, который мы сохраним под постом'