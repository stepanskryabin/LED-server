from pydantic import BaseModel
from pydantic import Field


class SupportForm(BaseModel):
    user_name: str
    date_time: int
    time_zone: str
    email: str
    message: str
    importance: int


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
    module_acl: str = Field(default='all',
                            title="Access level")
    group_name: str = Field(default='all',
                            title="User group")
    is_deleted: bool = Field(default=False,
                             title="status of the account")
    is_activated: bool = Field(default=False,
                               title="activation status of the account")


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
