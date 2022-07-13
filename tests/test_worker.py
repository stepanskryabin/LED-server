from src.db.worker import DBWorker


def db(id: int = None, name: str = None):
    db = DBWorker(db_name=':memory:')
    db.connect()
    db.create_record()
    query = db.get_user(_id=id, name=name)
    db.disconnect()
    return query

def test_get_by_name():
    result = db(name="Peter")
    assert result.is_created == True

def test_get_by_id():
    result = db(id=1)
    assert result.is_created == True
