from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel


class UserAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    login: str = Field(index=True)
    password: str
    is_deleted: bool
    is_activated: bool
    auth_id: str = Field(default=None)
