from typing import Any
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from jose import JWTError, jwt

from src.core.security import create_access_token
from src.core.security import SECRET_KEY
from src.core.security import ALGORITHM
from src.db.worker import DBWorker
from src.schemas.schemas import UserLogin


db = DBWorker()


class CredentialsError(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_401_UNAUTHORIZED,
                 detail: Any = "Could not validate credentials",
                 headers: dict = {"WWW-Authenticate": "Bearer"}) -> None:
        super().__init__(status_code=status_code,
                         detail=detail,
                         headers=headers)


def get_auth_token(user: UserLogin) -> str:
    token = create_access_token(data=user.dict(),
                                expires_delta=30)
    return token


def check_auth_token(token: str = Header()) -> None:
    payload: dict
    username: str

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise CredentialsError(detail="JWTError")
    else:
        username = payload.get("sub")
        if username is None:
            raise CredentialsError(detail="username error")

    user = db.get_user(name=username)
    if user.name is None:
        raise CredentialsError(detail="db user error")

    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
