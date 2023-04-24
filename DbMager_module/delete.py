from DbClasses import engine, tg_users, tg_user_settings, vk_groups, \
    tg_monitored_groups, tg_quick_answers, tg_access_key_vk
from datetime import datetime
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from other_module import logger
import check, get

"""
Сокращения 
id - id:int main объекта проверки (пишется только при доп аргументе)
us - user_id:int 
gr - group_id:int
domain - domain:str группы
tok - token:str 
"""


def quick_answer(answer_id: int) -> None:
    """Удаляет быстрый вариант ответа из бд(tg_quick_answers)"""
    conn = engine.connect()
    try:
        conn.execute(delete(tg_quick_answers).where(tg_quick_answers.c.id == answer_id))
        conn.commit()
    except IntegrityError:
        logger.error(f'{answer_id} не существует или не тот type')
    conn.close()


def group(group_id: int, conn=None) -> None:
    con = conn
    if not conn:
        con = engine.connect()
    try:
        con.execute(delete(vk_groups).where(vk_groups.c.id == group_id))

    except:
        pass



def subscribe_gr_us(group_id: int, user_id: int) -> None:
    """Удаляет подписку пользователя на группу бд(tg_monitored_groups)"""
    conn = engine.connect()
    try:
        conn.execute(delete(tg_monitored_groups).where(
            tg_monitored_groups.c.user_id == user_id).where(tg_monitored_groups.c.vk_group_id == group_id))
        if not check.group_exists_id(group_id):
            group(group_id, conn)
        conn.commit()
    except IntegrityError:
        logger.error(f'что-то с данными')
    conn.close()


def subscribe(subs_id: int) -> None:
    """Удаляет подписку пользователя на группу бд(tg_monitored_groups)"""
    conn = engine.connect()
    try:
        group_id = get.__group_id_by_sub_id(subs_id, conn)
        conn.execute(delete(tg_monitored_groups).where(tg_monitored_groups.c.id == subs_id))
        if not check.group_exists_id(group_id):
            group(group_id, conn)
        conn.commit()
    except IntegrityError:
        logger.error(f'что-то с данными')
    conn.close()


def token(t_id: int) -> None:
    """Удаляет токен по id"""
    conn = engine.connect()
    try:
        conn.execute(delete(tg_access_key_vk).where(tg_access_key_vk.c.id == t_id))
        conn.commit()
    except IntegrityError:
        logger.error(f'что-то с данными')
    conn.close()
