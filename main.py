from enum import Enum

from fastapi import FastAPI, Query, Cookie, status, HTTPException
from sqlalchemy.exc import MultipleResultsFound

from src.db.worker import DBWorker
from src.schemas.model import UserListIn, UserListOut
from src.schemas.model import SupportForm

app = FastAPI()

db = DBWorker()


class Model(str, Enum):
    first = "first"
    second = "second"


@app.get("/", tags=['main'])
async def get_root(skip: int = 0, limit: int = 10):
    if limit > 100:
        return "Error!"
    return f"Hello World skip={skip}, limit={limit}"


@app.on_event("startup")
def on_startup():
    db.connect()
    db.create_record()


@app.on_event("shutdown")
def on_shutdown():
    db.disconnect()


@app.get("/login", tags=['auth'])
async def login():
    return {"Log In": "not implemented"}


@app.get("/signin", tags=['auth'])
async def signin():
    return {"Sign In": "not implemented"}


@app.get("/user",
         response_model=UserListIn,
         tags=['users'])
async def userlist(username: str = Query(default=None,
                                         max_length=50,
                                         title="User name",
                                         description="Requested user name")):
    """
    Search user.
    """
    try:
        result = db.get_user_by_name(username)
    except MultipleResultsFound:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="BlaBlaBla")
    else:
        return result


@app.post("/user",
          response_model=UserListOut,
          status_code=status.HTTP_201_CREATED,
          tags=['users'])
async def add_user(item: UserListIn):
    """
    Add new user.
    """
    db.add_user(item)
    return item


@app.get("/support/{item}",
         tags=['support'])
async def get_support(item: Model, id: int):
    if item == Model.first and id <= 10:
        return db.get_by_id(id)
    elif item == Model.second and id <= 10:
        return {"result": "Second model"}
    else:
        return {"result": f"ID must be <= 10, not={id}"}


@app.post("/support/",
          response_model=SupportForm,
          status_code=status.HTTP_201_CREATED,
          tags=['support'])
async def post_support(item: SupportForm):
    db.add(user_name=item.user_name,
           date_time=item.date_time,
           time_zone=item.time_zone,
           email=item.email,
           message=item.message,
           importance=item.importance)
    return item
