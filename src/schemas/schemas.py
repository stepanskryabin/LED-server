from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


__all__ = ("User",
           "UserResponse",
           "UserRequest",
           "UserLogin",
           "UserRegister",
           "UserError",
           "InfoResponse")


# Hidden class, not used for work
class _UserLogin(BaseModel):
    login: str = Field(default=None,
                       title="User login name",
                       max_length=50)


class _UserName(BaseModel):
    name: str = Field(default=None,
                      title="User name",
                      max_length=50)


class _UserPassword(BaseModel):
    password: str = Field(default=None,
                          title="User password",
                          max_length=50)


class _UserAuth(BaseModel):
    auth_id: str = Field(default=None,
                         title='authentication token')


class _UserEmail(BaseModel):
    email: EmailStr = Field(default=None,
                            title="Contact email")


class _UserIsDeleted(BaseModel):
    is_deleted: bool = Field(default=False,
                             title="status of the account")


class _UserIsActivated(BaseModel):
    is_activated: bool = Field(default=False,
                               title="activation status of the account")


class _UserIsCreated(BaseModel):
    is_created: bool = Field(default=False,
                               title="create or not")


class _UserError(BaseModel):
    code: int =Field(default=None, title="Status code")
    detail: str = Field(default=None, title="Message text")


# Working schemas classes
class User(_UserName,
           _UserLogin,
           _UserEmail,
           _UserIsDeleted,
           _UserIsActivated):
    pass


class UserResponse(_UserName,
                   _UserLogin,
                   _UserEmail,
                   _UserIsDeleted,
                   _UserIsActivated):
    pass


class UserCreate(_UserName,
                 _UserLogin,
                 _UserEmail,
                 _UserPassword,
                 _UserIsDeleted,
                 _UserIsActivated):
    pass


class UserDBResult(_UserName,
                   _UserLogin,
                   _UserPassword,
                   _UserEmail,
                   _UserIsDeleted,
                   _UserIsActivated,
                   _UserIsCreated):

    class Config:
        orm_mode = True


class UserLogin(_UserName,
                _UserPassword):
    pass


class UserRegister(_UserName,
                   _UserPassword,
                   _UserEmail):
    pass

class UserAuth(_UserAuth):
    pass


class ErrorResponse(_UserError):
    pass


class InfoResponse(_UserError):
    pass
