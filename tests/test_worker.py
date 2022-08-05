from src.db.worker import DBWorker


class TestDatabase:
    def test_get_by_name(self, fx_db):
        result = fx_db.get_user(name="Test")
        assert result.is_created is True

    def test_get_by_name_2(self, fx_db):
        result = fx_db.get_user(name="Wrong")
        assert result.is_created is False
        assert result.name is None

    def test_get_by_id(self, fx_db):
        result = fx_db.get_user(_id=1)
        assert result.is_created is True

    def test_one_connection(self, fx_db):
        db = DBWorker()
        result = db.get_user(name="Test")
        assert result.is_created is True
