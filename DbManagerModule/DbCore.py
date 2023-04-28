from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm.session import sessionmaker, close_all_sessions

from other_module import CONFIG
from .DbClasses import Base


class Core:
    __engine = create_engine(CONFIG.DB_LINK)
    __async_engine = create_async_engine(CONFIG.ASYNC_DB_LINK)

    def __init__(self):
        try:
            self.create_db()
            self.__standard_session = self.get_new_session()
            self.__standard_async_session = self.get_new_async_session()
        finally:
            self.__close_all_session()

    def create_db(self):
        Base.metadata.create_all(self.__engine)

    def get_new_async_session(self):
        return async_sessionmaker(bind=self.__async_engine)()

    def get_new_session(self):
        return sessionmaker(bind=self.__engine)()

    def get_session(self):
        return self.__standard_session

    def get_async_session(self):
        return self.__standard_async_session

    def __close_all_session(self):
        self.__standard_session.close()
        close_all_sessions()


core = Core()
