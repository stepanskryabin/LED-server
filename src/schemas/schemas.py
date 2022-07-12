from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class User(BaseModel):
    name: str = Field(default=None,
                      title="User name",
                      max_length=50)
    login: str = Field(default=None,
                       title="User login name",
                       max_length=50)
    password: str = Field(default=None,
                          title="User password",
                          max_length=50)
    email: EmailStr = Field(default=None,
                            title="Contact email")
    is_deleted: bool = Field(default=False,
                             title="status of the account")
    is_activated: bool = Field(default=False,
                               title="activation status of the account")


class UserResponse(User):
    is_created: bool = Field(default=False,
                               title="create or not")

    class Config:
        orm_mode = True


class UserRequest(User):
    auth_id: str = Field(default=None,
                         title='authentication token')



class UserLogin(BaseModel):
    name: str = Field(default=None,
                      title="Unique user name",
                      max_length=50)
    password: str = Field(default=None,
                          title="User password",
                          max_length=50)


class UserRegister(UserLogin):
    email: EmailStr = Field(default=None,
                            title="Contact email")
