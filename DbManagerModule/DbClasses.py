from sqlalchemy import \
    (Text, Column, String, Integer, Boolean, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    available = Column(Boolean, default=True)
    time_zone = Column(Integer, default=3)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    domain = Column(String, nullable=False)
    serviceable = Column(Boolean, default=True)
    last_post_id = Column(Integer, default=0)


class VkApiToken(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    token = Column(Text, nullable=False)
    nickname = Column(String, nullable=False)
    serviceable = Column(Boolean, default=True)


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    token_id = Column(Integer, ForeignKey('tokens.id', ondelete="CASCADE"), nullable=False)


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    nickname = Column(String)

