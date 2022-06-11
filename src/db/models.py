from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class SupportType(Base):
    __tablename__ = "Type of request for support"

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    date_time = Column(Integer)
    time_zone = Column(String)
    email = Column(String)
    message = Column(String)
    importance = Column(Integer)

    def __repr__(self):
        return f"SupportType(id={self.id}, user={self.user_name})"
