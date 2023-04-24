from DbClasses import engine, tg_users, tg_user_settings, vk_groups, \
    tg_monitored_groups, tg_quick_answers, tg_access_key_vk
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from other_module import logger

"""
Сокращения 
id - id:int main объекта проверки
us - user_id:int 
gr - group_id:int
domain - domain:str группы
tok - token:str 
"""


def user_setting(user_id: int, time_zone: int) -> None:
    """Обновляет часовой пояс пользователя"""
    conn = engine.connect()
    try:
        conn.execute(update(tg_user_settings).where(tg_user_settings.c.user_id == user_id).values(time_zone=time_zone))
        conn.commit()
    except IntegrityError:
        logger.error(f'user_id существует? а типы сходятся? (user_id, time_zone)({user_id, time_zone})')
    conn.close()


def user(user_id: int, **kwargs) -> None:
    """Обновляет часть данных пользователя"""
    conn = engine.connect()
    try:
        conn.execute(update(tg_users).where(tg_users.c.id == user_id).values(**kwargs))
        conn.commit()
    except IntegrityError:
        logger.error(f'user_id существует? а типы сходятся? {kwargs}')
    conn.close()


def quick_answer(answer_id: int, user_id: int, **kwargs) -> None:
    """Обновляет часть данных быстрого ответа"""
    conn = engine.connect()
    try:

        conn.execute(update(tg_quick_answers).where(tg_quick_answers.c.id == answer_id).where(
            tg_quick_answers.c.user_id == user_id).values(**kwargs))
        conn.commit()
    except IntegrityError:
        logger.error(
            f'quick_answer_id существует? а типы сходятся? (quick_answer_id, user_id)({answer_id, user_id, kwargs})')
    conn.close()


def token(token_id: int, user_id: int, **kwargs) -> None:
    """Обновляет часть данных tg_access_key_vk"""
    conn = engine.connect()
    try:
        conn.execute(update(tg_access_key_vk).where(tg_access_key_vk.c.id == token_id).where(
            tg_access_key_vk.c.user_id == user_id).values(**kwargs))
        conn.commit()
    except IntegrityError:
        logger.error(f'token_id; user_id существуют? а типы сходятся? (token_id, user_id) {token_id, user_id, kwargs}')
    conn.close()


def subscribe_id_us(sub_id: int, user_id: int, **kwargs) -> None:
    """Обновляет часть данных tg_monitored_groups"""
    try:
        conn = engine.connect()
        conn.execute(update(tg_monitored_groups).where(
            tg_monitored_groups.c.id == sub_id).where(tg_monitored_groups.c.user_id == user_id).values(**kwargs))
        conn.commit()
        conn.close()
    except IntegrityError:
        logger.error(f'sub_id существуют? а типы сходятся? (sub_id) {sub_id, kwargs}')


def subscribe_gr_us(group_id: int, user_id: int, **kwargs) -> None:
    """Обновляет часть данных tg_monitored_groups"""
    try:
        conn = engine.connect()
        conn.execute(update(tg_monitored_groups).where(tg_monitored_groups.c.vk_group_id == group_id).where(
            tg_monitored_groups.c.user_id == user_id).values(**kwargs))
        conn.commit()
        conn.close()
    except IntegrityError:
        logger.error(f'sub_id существуют? а типы сходятся? (gr_id) {group_id, kwargs}')


def group(group_id: int, **kwargs) -> None:
    """Обновляет часть данных vk_groups оп group_id"""
    conn = engine.connect()
    try:
        conn.execute(update(vk_groups).where(vk_groups.c.id == group_id).values(**kwargs))
        conn.commit()
    except IntegrityError:
        logger.error(f'gr_id существуют? а типы сходятся? (gr_id) {group_id, kwargs}')
    conn.close()


def group_domain(domain: str, **kwargs) -> None:
    """Обновляет часть данных vk_groups по domain"""
    conn = engine.connect()
    try:
        conn.execute(update(vk_groups).where(vk_groups.c.idomaind == domain).values(**kwargs))
        conn.commit()
    except IntegrityError:
        logger.error(f'domain существуют? а типы сходятся? (domain) {domain, kwargs}')
    conn.close()
