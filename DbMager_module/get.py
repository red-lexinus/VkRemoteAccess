from DbClasses import engine, tg_users, tg_user_settings, vk_groups, \
    tg_monitored_groups, tg_quick_answers, tg_access_key_vk
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from other_module import logger


def __group_id_by_sub_id(subs_id: int, conn) -> int | None:
    """Возвращает id группы на которую оформлена подписка"""
    res = conn.execute(select(tg_monitored_groups.c.vk_group_id).where(
        tg_monitored_groups.c.id == subs_id)).fetchall()
    if res:
        return res[0][0]
    return None

