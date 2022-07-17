from typing import Any

from fastapi import Depends, Header
from fastapi import HTTPException
from fastapi import status
from jose import JWTError, jwt

from src.core.security import oauth2_scheme
from src.core.security import SECRET_KEY
from src.core.security import ALGORITHM
from src.db.worker import DBWorker


db = DBWorker()


class CredentialsError(HTTPException):
    def __init__(self,
                 status_code: int = status.HTTP_401_UNAUTHORIZED,
                 detail: Any = "Could not validate credentials",
                 headers: dict = {"WWW-Authenticate": "Bearer"}) -> None:
        super().__init__(status_code=status_code,
                         detail=detail,
                         headers=headers)


def get_auth_token(token: str = Depends(oauth2_scheme)) -> None:
    payload: dict
    username: str

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise CredentialsError
    else:
        username = payload.get("sub")
        if username is None:
            raise CredentialsError

    user = db.get_user(name=username)
    if user.name is None:
        raise CredentialsError

    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")


def check_auth_token(token: str = Header()) -> None:
    payload: dict
    username: str

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise CredentialsError
    else:
        username = payload.get("sub")
        if username is None:
            raise CredentialsError

    user = db.get_user(name=username)
    if user.name is None:
        raise CredentialsError

    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
