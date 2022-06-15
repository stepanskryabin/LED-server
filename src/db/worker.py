import time

from sqlmodel import create_engine
from sqlmodel import select
from sqlmodel import Session
from sqlmodel import SQLModel

from src.db.models import SupportType


class DBWorker:
    def __init__(self,
                 db_name: str = 'db.sqlite',
                 engine: str = 'sqlite',
                 _echo: bool = False,
                 _check_same_thread: bool = False):
        self.uri = "".join((engine, ":///", db_name))
        self._connect_args = {"check_same_thread": _check_same_thread}
        self._engine = create_engine(self.uri,
                                     echo=_echo,
                                     connect_args=self._connect_args)
        self._session = Session(self._engine)
        self._sql = SQLModel.metadata

    def connect(self):
        self._sql.create_all(self._engine)

    def disconnect(self):
        self._session.close_all()

    def create_record(self):
        with self._session as session:
            statment = SupportType(user_name="Test1",
                                   date_time=int(time.time()),
                                   time_zone='Europe/Moscow',
                                   email='test@test.com',
                                   message="Help me, Obi-Wan Kenobi!",
                                   importance=1)
            session.add(statment)
            session.commit()
            session.refresh(statment)
            session.close()

    def get_by_id(self,
                  _id: int):
        statment = select(SupportType).where(SupportType.id == _id)
        return self._session.exec(statment).one()

    def add(self,
            user_name: str,
            date_time: int,
            email: str,
            message: str,
            time_zone: str = 'Europe/Moscow',
            importance: int = 1):
        row = SupportType(user_name=user_name,
                          date_time=date_time,
                          time_zone=time_zone,
                          email=email,
                          message=message,
                          importance=importance)
        with self._session as session:
            session.add(row)

        self._session.commit()

    def __del__(self):
        self._session.close()
