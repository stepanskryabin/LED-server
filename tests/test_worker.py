

class TestDatabase:
    def test_get_by_name(self, db):
        result = db.get_user(name="Peter")
        assert result.is_created == True

    def test_get_by_id(self, db):
        result = db.get_user(_id=1)
        assert result.is_created == True
