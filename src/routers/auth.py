from fastapi import APIRouter
from fastapi import status
from fastapi import Response

from src.db.worker import DBWorker
from src.schemas.schemas import ErrorResponse
from src.schemas.schemas import InfoResponse
from src.schemas.schemas import UserAuth
from src.schemas.schemas import UserLogin
from src.schemas.schemas import UserRegister


router = APIRouter()
db = DBWorker()


@router.post("/login",
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


@router.post("/signin",
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
