from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
from other_module import CONFIG

metadata = MetaData()
engine = create_engine(CONFIG.DB_LINK)

vk_groups = \
    Table('vk_groups', metadata,
          Column('id', Integer(), primary_key=True),
          Column('domain', String(CONFIG.MIN_STR), nullable=False),
          Column('serviceable', Boolean(), nullable=False, default=True),
          Column('last_post_id', Integer())
          )

tg_users = \
    Table('tg_users', metadata,
          Column('id', Integer(), primary_key=True),
          Column('nickname', String(CONFIG.MIN_STR), nullable=False),
          Column('available', Boolean, default=True),
          Column('reg_date', DateTime, nullable=False),
          Column('max_tokens', Integer(), nullable=False, default=CONFIG.MAX_TOKENS_DEFAULT),
          Column('max_public', Integer(), nullable=False, default=CONFIG.MAX_PUBLIC_DEFAULT),
          )

tg_user_settings = \
    Table('tg_user_settings', metadata,
          Column('user_id', ForeignKey('tg_users.id'), primary_key=True),
          Column('time_zone', Integer(), default=3),
          )

tg_access_key_vk = \
    Table('tg_access_key_vk', metadata,
          Column('id', Integer(), primary_key=True, autoincrement=True),
          Column('user_id', ForeignKey('tg_users.id'), nullable=False),
          Column('token', Text(), nullable=False),
          Column('nickname', String(CONFIG.NORMAL_STR), nullable=False, default='вк-акк'),
          Column('serviceable', Boolean(), nullable=False, default=True),
          )

tg_monitored_groups = \
    Table('tg_monitored_groups', metadata,
          Column('id', Integer(), primary_key=True, autoincrement=True),
          Column('vk_group_id', ForeignKey('vk_groups.id'), nullable=False),
          Column('user_id', ForeignKey('tg_users.id'), nullable=False),
          Column('token_id', ForeignKey('tg_access_key_vk.id'), nullable=False),
          )

tg_quick_answers = \
    Table('tg_quick_answers', metadata,
          Column('id', Integer(), primary_key=True, autoincrement=True),
          Column('user_id', ForeignKey('tg_users.id'), nullable=False),
          Column('message', String(CONFIG.MAX_STR), nullable=False),
          Column('short_txt', String(CONFIG.MIN_STR)),
          )

metadata.create_all(engine)
