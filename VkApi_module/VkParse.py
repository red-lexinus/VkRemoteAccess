import requests

from other_module import CONFIG

start_link = CONFIG.START_LINK
version = CONFIG.VERSION


def new_comment(group_id: int, post_id: int, message: str, token: str):
    """Сохраняет текстовый комментарий под постом, и возвращает успешно ли это выполнено"""
    link = f"{start_link}wall.createComment?owner_id={-group_id}&post_id={post_id}&" \
           f"access_token={token}&message={message}&{version}"
    req = requests.get(link).json()
    return req




