from pydantic import BaseModel
from pydantic import Field


class UserListIn(BaseModel):
    name: str = Field(default=None,
                      title="User name",
                      max_length=100)
    login: str = Field(default=None,
                       title="User log in name",
                       max_length=100)
    password: str = Field(default=None,
                          title="User password",
                          max_length=100)
    is_deleted: bool = Field(default=False,
                             title="status of the account")
    is_activated: bool = Field(default=False,
                               title="activation status of the account")
    auth_id: str = Field(default=None,
                         title='authentication token')


class UserListOut(BaseModel):
    name: str = Field(default=None,
                      title="User name",
                      max_length=100)
    login: str = Field(default=None,
                       title="User log in name",
                       max_length=100)
    is_deleted: bool = Field(default=False,
                             title="status of the account")
    is_activated: bool = Field(default=False,
                               title="activation status of the account")
    is_created: bool = Field(default=False,
                               title="create or not")
    
    class Config:
        orm_mode = True
