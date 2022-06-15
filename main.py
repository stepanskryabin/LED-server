from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from src.db.worker import DBWorker

app = FastAPI()

db = DBWorker()


class Item(BaseModel):
    user_name: str
    date_time: int
    time_zone: str
    email: str
    message: str
    importance: int = 0


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


@app.post("/support/")
async def post_support(item: Item):
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
