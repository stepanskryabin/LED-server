import unittest

from src.db.worker import DBWorker


class TestDBWorker(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DBWorker(db_name=':memory:')
        self.db.connect()

    def tearDown(self) -> None:
        self.db.disconnect()

    def test_get_by_name(self):
        self.db.create_record()
        result = self.db.get_user(name="Peter")
        self.assertTrue(result.is_created)

    def test_get_by_id(self):
        self.db.create_record()
        result = self.db.get_user(_id=1)
        self.assertTrue(result.is_created)
