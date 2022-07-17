import pytest

from src.db.worker import DBWorker


@pytest.fixture(scope="class")
def db():
    database = DBWorker(db_name=":memory:")
    database.connect()
    database.create_record()
    yield database
    database.disconnect()


@pytest.fixture(scope="class")
def headers() -> dict:
    return {"token": "token"}


@pytest.fixture(scope="class")
def json() -> dict:
    return {"name": "PeterTheOne",
            "login": "peter_the_one",
            "password": "123456",
            "email": "peter@theone.rus",
            "is_deleted": False,
            "is_activated": True}
