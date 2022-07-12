from enum import Enum

from fastapi import FastAPI, Query, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import MultipleResultsFound

from src.db.worker import DBWorker
from schemas.schemas import UserListIn, UserListOut
from src.settings import ABOUT, origins

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

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
