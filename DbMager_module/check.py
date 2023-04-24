from DbClasses import engine, tg_users, vk_groups, tg_monitored_groups, tg_access_key_vk
from sqlalchemy import select

conn = engine.connect()

"""
Сокращения 
id - id:int main объекта проверки
us - user_id:int 
domain - domain:str группы
tok - token:str 
"""


def user_exists_id(user_id: int) -> bool:
    """Проверяет существует ли пользователь"""
    return bool(conn.execute(select(tg_users).where(tg_users.c.id == user_id)).fetchall())


def group_exists_id(group_id: int) -> bool:
    """Проверяет существует ли группа в бд(vk_groups) по group_id"""""
    return bool(conn.execute(select(vk_groups).where(vk_groups.c.id == group_id)).fetchall())


def group_exists_domain(group_domain: str) -> bool:
    """Проверяет существует ли группа в бд(vk_groups) по group_domain"""""
    return bool(conn.execute(select(vk_groups).where(vk_groups.c.domain == group_domain)).fetchall())


def subs_exists_id(group_id: int) -> bool:
    """Проверяет существует ли подписки на группу"""
    return bool(conn.execute(select(tg_monitored_groups).where(
        tg_monitored_groups.c.vk_group_id == group_id)).fetchall())


def subs_exists_us_id(user_id: int, group_id: int) -> bool:
    """Проверяет существует ли у пользователя подписка на группу"""
    return bool(conn.execute(select(tg_monitored_groups).where(
        tg_monitored_groups.c.user_id == user_id).where(tg_monitored_groups.c.vk_group_id == group_id)).fetchall())


def token_exists_id(token_id: int) -> bool:
    """Проверяет существует ли token по token_id"""
    return bool(conn.execute(select(tg_access_key_vk).where(tg_access_key_vk.c.id == token_id)).fetchall())


def token_exists_us(user_id: int) -> bool:
    """Проверяет существует ли у пользователя token"""
    return bool(conn.execute(select(tg_access_key_vk).where(tg_access_key_vk.c.user_id == user_id)).fetchall())


def serviceable_token_id(token_id: int) -> bool:
    """Проверяет токен на работоспособность"""
    return bool(conn.execute(select(tg_access_key_vk).where(
        tg_access_key_vk.c.id == token_id).where(tg_access_key_vk.c.serviceable)).fetchall())


def serviceable_token_us(user_id: int) -> bool:
    """Проверяет токены пользователя на работоспособность"""
    return bool(conn.execute(select(tg_access_key_vk).where(
        tg_access_key_vk.c.user_id == user_id).where(tg_access_key_vk.c.serviceable)).fetchall())


def token_exists_us_tok(user_id: int, token: str) -> bool:
    """Проверяет существует ли у пользователя конкретный token (поиск по token:str)"""
    return bool(conn.execute(select(tg_access_key_vk).where(
        tg_access_key_vk.c.user_id == user_id).where(tg_access_key_vk.c.token == token)).fetchall())
