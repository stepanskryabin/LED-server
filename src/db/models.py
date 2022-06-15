from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel


class SupportType(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(index=True)
    date_time: int
    time_zone: str
    email: str
    message: str
    importance: int
