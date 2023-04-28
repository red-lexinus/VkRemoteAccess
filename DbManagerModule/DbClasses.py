from sqlalchemy import \
    (Text, Column, String, Integer, Boolean, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    available = Column(Boolean, default=True)
    time_zone = Column(Integer, default=3)

    def __repr__(self):
        return f"user({self.id}; {self.available}; {self.time_zone})"


class UserRights(Base):
    __tablename__ = 'users_rights'
    id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    max_tokens = Column(Integer, nullable=False)
    max_subs = Column(Integer, nullable=False)
    donate = Column(Boolean, default=False)

    def __repr__(self):
        return f"users_rights({self.id}; {self.max_tokens}; {self.max_subs}; {self.donate})"


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    domain = Column(String, nullable=False)
    serviceable = Column(Boolean, default=True)
    last_post_id = Column(Integer, default=0)

    def __repr__(self):
        return f"group({self.id}; {self.domain}; {self.serviceable}; {self.last_post_id})"


class VkApiToken(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    token = Column(Text, nullable=False)
    nickname = Column(String, nullable=False)
    serviceable = Column(Boolean, default=True)

    def __repr__(self):
        return f"token({self.id}; {self.user_id}; {self.serviceable}; {self.nickname})"


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    token_id = Column(Integer, ForeignKey('tokens.id', ondelete="CASCADE"), nullable=False)
    nickname = Column(String, default="Группа")

    def __repr__(self):
        return f"subscription({self.id}; {self.user_id}; {self.group_id}; {self.token_id})"


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    nickname = Column(String)

    def __repr__(self):
        return f"answer({self.id}; {self.user_id}; {self.nickname}; {self.message})"
