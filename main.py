from fastapi import FastAPI, Query, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.db.worker import DBWorker
from src.schemas.schemas import ErrorResponse
from src.schemas.schemas import UserAuth
from src.schemas.schemas import UserLogin
from src.schemas.schemas import InfoResponse
from src.schemas.schemas import UserRegister
from src.schemas.schemas import UserResponse
from src.schemas.schemas import UserRequest
from src.settings import ABOUT, origins

app = FastAPI()

additional_responses = {
    401: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

db = DBWorker()


@app.get("/", tags=['main'])
async def get_root(skip: int = 0,
                   limit: int = 10):
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
          response_model=UserAuth,
          responses=additional_responses,
          tags=['auth'])
async def login(old_user: UserLogin):
    """
    The user login procedure for the application.
    """

    if old_user.password == db.get_user(name=old_user.name).password:
        return UserAuth(auth_id="auth_id")
    else:
        return ErrorResponse(code=status.HTTP_401_UNAUTHORIZED,
                         detail="User is unknow")


@app.post("/signin",
          status_code=status.HTTP_201_CREATED,
          response_model=InfoResponse,
          responses=additional_responses,
          tags=['auth'])
async def signin(new_user: UserRegister):
    """
    The user registration procedure in the application.
    """

    try:
        db.add_user(new_user)
    except Exception:
        raise ErrorResponse(code=status.HTTP_409_CONFLICT,
                        detail="Unknow error")
    else:
        return InfoResponse(code=status.HTTP_201_CREATED,
                            detail="User is created")


@app.get("/user",
         status_code=status.HTTP_200_OK,
         response_model=UserResponse,
         responses=additional_responses,
         tags=['admin_panel'])
async def userlist(username: str = Query(default=None,
                                         max_length=50,
                                         title="User name",
                                         description="Requested user name")):
    """
    Search user.
    """

    result = db.get_user(name=username)
    if result.name is None:
        raise ErrorResponse(code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")
    else:
        return result


@app.post("/user",
          response_model=UserResponse,
          status_code=status.HTTP_201_CREATED,
          responses=additional_responses,
          tags=['admin_panel'])
async def add_user(item: UserRequest):
    """
    Add new user.
    """

    try:
        db.add_user(item)
    except Exception:
        raise ErrorResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Unknow server error")
    else:
        return item
