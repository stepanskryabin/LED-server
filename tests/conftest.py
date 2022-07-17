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
    return {"token":
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUZXN0IiwiZXhwIjoxNjU4MDczODIzfQ.dhr_mc-MxtjjN0F5g9i_S1yz4D-WuOqT3HGNROGIRxY"}


@pytest.fixture(scope="class")
def json() -> dict:
    return {"name": "PeterTheOne",
            "login": "peter_the_one",
            "password": "123456",
            "email": "peter@theone.rus",
            "is_deleted": False,
            "is_activated": True}
