from typing import Optional
from sqlalchemy import table

from sqlmodel import Field
from sqlmodel import SQLModel
from sqlmodel import Relationship


class SupportType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(index=True)
    date_time: int
    time_zone: str
    email: str = Field(index=True)
    message: str
    importance: int


# class ModuleAcl(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name_acl: str
#     users: list['UserAccount'] = Relationship(back_populates='moduleacl')


# class UserGroup(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name_group: str
#     users: list['UserAccount'] = Relationship(back_populates='usergroup')


class UserAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    login: str = Field(index=True)
    password: str
    # id_acl: Optional[int] = Field(default=None, foreign_key='moduleacl.id')
    # module_acl: Optional[ModuleAcl] = Relationship(back_populates='users')
    # id_group: Optional[int] = Field(default=None, foreign_key='usergroup.id')
    # group_name: Optional[UserGroup] = Relationship(back_populates='users')
    module_acl: str
    group_name: str
    is_deleted: str
    is_activated: int



