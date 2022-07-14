import pytest

from src.db.worker import DBWorker


@pytest.fixture(scope="class")
def db():
    database = DBWorker(db_name=':memory:')
    database.connect()
    database.create_record()
    yield database
    database.disconnect()
