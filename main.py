from enum import Enum

from fastapi import FastAPI, Query, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import MultipleResultsFound

from src.db.worker import DBWorker
from src.schemas.schemas import UserLogin, UserRegister, UserRequest, UserResponse
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


@app.post("/login",
          status_code=status.HTTP_202_ACCEPTED,
          tags=['auth'])
async def login(old_user: UserLogin):
    """
    The user login procedure for the application.
    """

    if old_user.password == db.get_user(name=old_user.name).password:
        auth_id = "auth_id"
        return {"auth_id": auth_id}

    return {"Login": "User unknown!"}


@app.post("/signin",
          status_code=status.HTTP_201_CREATED,
          tags=['auth'])
async def signin(new_user: UserRegister):
    """
    The user registration procedure in the application.
    """

    try:
        db.add_user(new_user)
    except Exception:
        return {"Sign In": "Unknown error"}
    else:
        return {"Sign In": "Ok"}


@app.get("/user",
         response_model=UserResponse,
         tags=['admin_panel'])
async def userlist(username: str = Query(default=None,
                                         max_length=50,
                                         title="User name",
                                         description="Requested user name")):
    """
    Search user.
    """

    try:
        result = db.get_user(name=username)
    except MultipleResultsFound:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="BlaBlaBla")
    else:
        return result


@app.post("/user",
          response_model=UserResponse,
          status_code=status.HTTP_201_CREATED,
          tags=['admin_panel'])
async def add_user(item: UserRequest):
    """
    Add new user.
    """

    db.add_user(item)
    return item
