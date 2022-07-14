from fastapi import FastAPI, Query, status, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from src.db.worker import DBWorker
from src.schemas.schemas import ErrorResponse
from src.schemas.schemas import UserAuth
from src.schemas.schemas import UserLogin
from src.schemas.schemas import InfoResponse
from src.schemas.schemas import UserRegister
from src.schemas.schemas import UserResponse
from src.schemas.schemas import UserCreate
from src.settings import ABOUT, origins


app = FastAPI()
db = DBWorker()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"])


@app.on_event("startup")
def on_startup():
    db.connect()
    db.create_record()


@app.on_event("shutdown")
def on_shutdown():
    db.disconnect()


@app.get("/",
         tags=['Home'])
async def home_page(skip: int = 0,
                    limit: int = 10):
    if limit > 100:
        return "Error!"
    return f"Hello World skip={skip}, limit={limit}"


@app.post("/login",
          status_code=status.HTTP_202_ACCEPTED,
          responses={401: {"model": ErrorResponse}},
          tags=['Auth'],
          description="The authorization procedure in the application.")
async def login(user: UserLogin, response: Response):
    """
    The user login procedure for the application.
    """

    if user.password == db.get_user(name=user.name).password:
        return UserAuth(auth_id="auth_id")
    else:
        response.status_code = code = status.HTTP_401_UNAUTHORIZED
        return ErrorResponse(code=code, detail="User is unknow")


@app.post("/signin",
          status_code=status.HTTP_201_CREATED,
          response_model=InfoResponse,
          responses={409: {"model": ErrorResponse}},
          tags=['Auth'])
async def signin(new_user: UserRegister, response: Response):
    """
    The user registration procedure in the application.
    """

    try:
        db.add_user(new_user)
    except Exception:
        response.status_code = code = status.HTTP_409_CONFLICT
        raise ErrorResponse(code=code,
                            detail="Unknow error")
    else:
        return InfoResponse(code=status.HTTP_201_CREATED,
                            detail="User is created")


@app.get("/user",
         status_code=status.HTTP_200_OK,
         response_model=UserResponse,
         responses={404: {"model": ErrorResponse}},
         tags=['Admin panel'])
async def userlist(response: Response,
                   username: str = Query(default=None,
                                         max_length=50,
                                         title="User name",
                                         description="Requested user name")):
    """
    Search user.
    """

    result = db.get_user(name=username)
    if result.name is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise ErrorResponse(code=response.status_code,
                            detail="User not found")
    else:
        return result


@app.post("/user",
          response_model=UserResponse,
          status_code=status.HTTP_201_CREATED,
          responses={500: {"model": ErrorResponse}},
          tags=['Admin panel'])
async def add_user(item: UserCreate, response: Response):
    """
    Add new user.
    """

    try:
        db.add_user(item)
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise ErrorResponse(code=response.status_code,
                            detail="Unknow server error")
    else:
        return item
