from datetime import timedelta
from datetime import datetime
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from src.db.worker import DBWorker
from src.schemas.schemas import UserDBResult


db = DBWorker()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "31465e473b6f7f661058f3e6c5bd6fc13c889eac95726084dde2b29770639f3c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return True
    # return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str,
                      password: str) -> UserDBResult | bool:
    user = db.get_user(name=username)

    if user.name is None:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict,
                        expires_delta: timedelta = None) -> Any:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
