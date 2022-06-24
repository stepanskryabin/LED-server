from enum import Enum

from fastapi import FastAPI

from src.db.worker import DBWorker
from src.schemas.model import UserList
from src.schemas.model import SupportForm

app = FastAPI()

db = DBWorker()


class Model(str, Enum):
    first = "first"
    second = "second"


@app.get("/")
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


@app.get("/login")
async def login():
    return {"Log In": "not implemented"}


@app.get("/signin")
async def signin():
    return {"Sign In": "not implemented"}


@app.get("/user")
async def userlist(username):
    result = db.get_user_by_name(username)
    return {"result": result}


@app.post("/user")
async def add_user(item: UserList):
    db.add_user(item)
    return {"result": "OK"}


@app.post("/support/")
async def post_support(item: SupportForm):
    db.add(user_name=item.user_name,
           date_time=item.date_time,
           time_zone=item.time_zone,
           email=item.email,
           message=item.message,
           importance=item.importance)
    return item


@app.get("/support/{item}")
async def get_support(item: Model, id: int):
    if item == Model.first and id <= 10:
        return db.get_by_id(id)
    elif item == Model.second and id <= 10:
        return {"result": "Second model"}
    else:
        return {"result": f"ID must be <= 10, not={id}"}
