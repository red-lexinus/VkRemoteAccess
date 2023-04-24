from DbClasses import engine, tg_users, tg_user_settings, vk_groups, \
    tg_monitored_groups, tg_quick_answers, tg_access_key_vk
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from other_module import logger
import check


def new_tg_user(user_id: int, nickname: str = 'некто') -> None:
    """
    Сохраняет нового пользователя (бд - tg_users).
    Также создаёт настройку его акк (бд - tg_user_settings)
    """
    user = {
        'id': user_id,
        'nickname': nickname,
        'reg_date': datetime.now(),
    }
    conn = engine.connect()
    try:
        conn.execute(insert(tg_users), user)
        conn.execute(insert(tg_user_settings), {'user_id': user_id})
        conn.commit()
    except IntegrityError:
        logger.error(f'{nickname}(id:{user_id}) уже сохранён в базу данных!')
    conn.close()


def new_group(group_id: int, group_domain: str, last_post_id=0) -> None:
    """
    Сохраняет паблик в общий список пабликов(бд - vk_groups)
    """
    group = {
        'id': group_id,
        'domain': group_domain,
        'last_post_id': last_post_id,
    }
    conn = engine.connect()
    try:
        conn.execute(insert(vk_groups), group)
        conn.commit()
    except IntegrityError:
        logger.error(f'группа(id:{group_id}) уже сохранёна в базу данных!')
    conn.close()


def new_subscribe(group_id: int, user_id: int, token_id: int, domain: str) -> None:
    """
    Сохраняет паблик в подписках у пользователя(бд - tg_monitored_groups),
    если этого паблика нет в общем списке пабликов, тогда сохраняет (бд - vk_groups).
    """
    subs = {
        'id': group_id,
        'user_id': user_id,
        'token_id': token_id,
        'domain': domain
    }
    conn = engine.connect()
    try:
        conn.execute(insert(tg_monitored_groups), subs)
        if not check.group_exists_id(group_id):
            # Сохраняет паблик в общий список пабликов
            conn.execute(insert(vk_groups), subs)
        conn.commit()
    except IntegrityError:
        logger.error(f'группа(id:{group_id}) уже сохранена в базу данных!')
    conn.close()


def new_quick_answer(user_id: int, message: str, short_txt: str or None = None) -> None:
    """Создаёт новый быстрый ответ(бд - tg_quick_answers)"""
    quick_answer = {
        'user_id': user_id,
        'message': message,
        'short_txt': short_txt,
    }
    conn = engine.connect()
    try:
        conn.execute(insert(tg_quick_answers), quick_answer)
        conn.commit()
    except IntegrityError:
        logger.error(f'Проверь user_id({user_id}) существует? Тогда хз в чём баг, может ввёл не те данные?')
    conn.close()


def new_token(user_id: int, token: str, nickname: str) -> None:
    """Сохраняет новый токен в бд(tg_access_key_vk)"""
    token = {
        'user_id': user_id,
        'token': token,
        'nickname': nickname,
    }
    conn = engine.connect()
    try:
        conn.execute(insert(tg_access_key_vk), token)
        conn.commit()
    except IntegrityError:
        logger.error(f'Проверь user_id({user_id}) существует? Тогда хз в чём баг, может ввёл не те данные?')
    conn.close()
