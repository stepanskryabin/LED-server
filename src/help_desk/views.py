import ujson
from sqlalchemy.exc import NoResultFound

from src.db.worker import DBWorker
from src.help_desk.api.model import SupportForm

db = DBWorker()
db.connect()


async def get_support_page(_input: int):
    try:
        dbquery = db.get_by_id(_input)
    except NoResultFound as err:
        dbquery = "Blank datatase"

    return {"result": dbquery}


async def post_support_page(_input: str):
    input = SupportForm.parse_obj(ujson.loads(_input))
    result = db.add(user_name=input.user_name,
                    date_time=input.date_time,
                    email=input.email,
                    message=input.message)
    return {"result": result}
