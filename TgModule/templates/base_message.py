from VkApiModule.ParseClasses import VkGroupInfo


def unknown_handler(msg: str) -> str:
    return f'Хм, вернём ваше сообщение:\n{msg}'


def none_token() -> str:
    return 'У вас нет токена! создайте его пожалуйста'


def none_group_url() -> str:
    return 'Скорее всего вы отправили не корректную ссылку на вк группу'


def failed_check_group() -> str:
    return 'Ошибочка, либо группы нет, либо ваши токены не имеют доступа к этой группе'


def check_group(group_data: VkGroupInfo) -> str:
    return f'{group_data.name}'
