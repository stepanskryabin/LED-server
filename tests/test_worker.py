

class TestDatabase:
    def test_get_by_name(self, db):
        result = db.get_user(name="Peter")
        assert result.is_created is True

    def test_get_by_name_2(self, db):
        result = db.get_user(name="Wrong")
        assert result.is_created is False
        assert result.name is None

    def test_get_by_id(self, db):
        result = db.get_user(_id=1)
        assert result.is_created is True
