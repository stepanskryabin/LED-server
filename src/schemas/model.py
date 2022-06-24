from pydantic import BaseModel


class SupportForm(BaseModel):
    user_name: str
    date_time: int
    time_zone: str
    email: str
    message: str
    importance: int


class UserList(BaseModel):
    name: str
    login: str
    password: str
    module_acl: str
    group_name: str
    is_deleted: bool
    is_activated: bool
