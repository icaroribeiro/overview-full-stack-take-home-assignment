from contextlib import contextmanager

from sqlalchemy import Connection, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSessionManager:
    def __init__(self, conn_string: str):
        self.__engine = create_engine(url=conn_string)
        self.__sessionmaker = sessionmaker(autocommit=False, bind=self.__engine)

    @contextmanager
    def connect(self) -> Connection:
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise

    def close(self):
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        self.__engine.dispose()

        self.__engine = None
        self.__sessionmaker = None

    @contextmanager
    def session(self) -> Session:
        if self.__sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self.__sessionmaker() as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
