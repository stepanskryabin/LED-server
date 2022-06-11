import time

from sqlalchemy import create_engine
from src.db.models import Base
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import SupportType


class DBWorker:
    def __init__(self,
                 db_name: str = '/:memory:',
                 engine: str = 'sqlite',
                 _echo: bool = False):
        self.database = "".join((engine, "://", db_name))
        self.engine = create_engine(self.database,
                                    echo=_echo,
                                    future=True)
        self.base = Base()
        self.session = Session(self.engine)

    def connect(self):
        self._create_db()
        self._create_table()

    def _create_db(self):
        self.base.metadata.create_all(self.engine)

    def _create_table(self):
        with self.session as session:
            user_help_one = SupportType(user_name="Test1",
                                        date_time=int(time.time()),
                                        time_zone='Europe/Moscow',
                                        email='test@test.com',
                                        message="Help me, Obi-Wan Kenobi!",
                                        importance=1)
            session.add_all([user_help_one])
            session.commit()

    def get_by_id(self,
                  _id: int):
        stmt = select(SupportType).where(SupportType.id.is_(_id))
        return self.session.scalars(stmt).one()

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
        self.session.add(row)
        self.session.commit()

    def __del__(self):
        self.session.close()
