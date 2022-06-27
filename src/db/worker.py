import random
import time

from sqlmodel import create_engine
from sqlmodel import select
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlalchemy.exc import NoResultFound

from src.db.models import SupportType
from src.db.models import UserAccount
from src.schemas.model import UserListIn


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
            add_support = SupportType(user_name="".join(("Test1",
                                                         str(random.randint(0, 1000)))),
                                      date_time=int(time.time()),
                                      time_zone='Europe/Moscow',
                                      email='test@test.com',
                                      message="Help me, Obi-Wan Kenobi!",
                                      importance=1)
            add_user = UserAccount(name="".join(("Peter",
                                                  str(random.randint(0, 1000)))),
                                   login="Peter The Great",
                                   password="IMGREAT",
                                   module_acl='Russia',
                                   group_name='tsar',
                                   is_deleted=False,
                                   is_activated=True)
            session.add(add_support)
            session.add(add_user)
            session.commit()
            session.refresh(add_support)
            session.refresh(add_user)
            session.close()

    def get_by_id(self,
                  _id: int):
        statment = select(SupportType).where(SupportType.id == _id)
        return self._session.exec(statment).one()

    def get_user_by_name(self,
                         name: str):
        statment = select(UserAccount).where(UserAccount.name == name)
        try:
            dbquery = self._session.exec(statment).one()
        except NoResultFound:
            return None
        else:
            return dbquery

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

    def add_user(self,
                 user: UserListIn):
        user_account = UserAccount(name=user.name,
                                   login=user.login,
                                   password=user.password,
                                   module_acl=user.module_acl,
                                   group_name=user.group_name,
                                   is_deleted=user.is_deleted,
                                   is_activated=user.is_activated)
        with self._session as session:
            session.add(user_account)
        self._session.commit()

    def __del__(self):
        self._session.close()
