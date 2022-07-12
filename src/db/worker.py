import random

from sqlmodel import create_engine
from sqlmodel import select
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlalchemy.exc import NoResultFound

from src.db.models import UserAccount
from src.schemas.schemas import UserListIn
from src.schemas.schemas import UserListOut


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
            user = UserAccount(name="Peter",
                               login="".join(("Peter",
                                             str(random.randint(0, 1000)))),
                               password='123456',
                               is_deleted=False,
                               is_activated=True,
                               auth_id='auth_id')
            session.add(user)
            session.commit()
            session.refresh(user)
            session.close()

    def get_user(self,
                 _id: int = None,
                 name: str = None) -> UserListOut:
        if id is None and name is None:
            raise ValueError('You must specify id or name.')

        if name is not None:
            statment = select(UserAccount).where(UserAccount.name == name)
        else:
            statment = select(UserAccount).where(UserAccount.id == _id)

        try:
            dbquery = self._session.exec(statment).one()
        except NoResultFound:
            result = UserListOut()
        else:
            result = UserListOut.from_orm(dbquery)
            result.is_created = True

        return result

    def add_user(self,
                 user: UserListIn):
        user_account = UserAccount(name=user.name,
                                   login=user.login,
                                   password=user.password,
                                   is_deleted=user.is_deleted,
                                   is_activated=user.is_activated,
                                   auth_id=user.auth_id)
        with self._session as session:
            session.add(user_account)
        self._session.commit()

    def __del__(self):
        self._session.close()
