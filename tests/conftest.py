import os
from fastapi import Response
import pytest

from src.db.worker import DBWorker
from src.schemas.schemas import UserLogin, UserRegister
from src.schemas.schemas import Token


@pytest.fixture(scope="class")
def fx_db() -> None:
    database = DBWorker()
    database.connect()
    database.add_user(UserRegister(name="Test",
                                   password="Test",
                                   email="test@test.ru"))
    yield database
    database.disconnect()
    os.remove('db.sqlite')


@pytest.fixture(scope="class")
def fx_headers() -> dict:
    return {"token":
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZXN0IiwiZXhwIjoxNjU4MDczODIzfQ.dhr_mc-MxtjjN0F5g9i_S1yz4D-WuOqT3HGNROGIRxY"}


@pytest.fixture(scope="class")
def fx_json() -> dict:
    return {"name": "PeterTheOne",
            "login": "peter_the_one",
            "password": "123456",
            "email": "peter@theone.rus",
            "is_deleted": False,
            "is_activated": True}


@pytest.fixture(scope="class")
def fx_response() -> Response:
    result = Response(status_code=200)
    return result


@pytest.fixture(scope="class")
def fx_token() -> Token:
    return Token(access_token="test_token",
                 token_type="bearer")


@pytest.fixture(scope="class")
def fx_str_token() -> str:
    return "token"


@pytest.fixture(scope='class')
def fx_user() -> UserLogin:
    return UserLogin(name="Test",
                     password="Test")
