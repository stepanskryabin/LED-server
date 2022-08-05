from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Response
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.db.worker import DBWorker
from src.core.deps import get_auth_token
from src.core.security import authenticate_user
from src.core.security import create_access_token
from src.core.security import ACCESS_TOKEN_EXPIRE_MINUTES
from src.schemas.schemas import ErrorResponse
from src.schemas.schemas import InfoResponse
from src.schemas.schemas import UserAuth
from src.schemas.schemas import UserLogin
from src.schemas.schemas import UserRegister
from src.schemas.schemas import Token


router = APIRouter()
db = DBWorker()


def check_password(login_password, db_password) -> bool:
    return login_password == db_password


@router.post("/login",
             status_code=status.HTTP_202_ACCEPTED,
             responses={401: {"model": ErrorResponse}},
             tags=['Auth'],
             description="The authorization procedure in the application.")
async def login(user: UserLogin,
                response: Response):
    """
    The user login procedure for the application.
    """

    db_user = db.get_user(name=user.name)
    if check_password(user.password, db_user.password):
        token = get_auth_token(user)
        return UserAuth(auth_id=token)
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
        return ErrorResponse(code=code,
                             detail="Unknow error")
    else:
        return InfoResponse(code=status.HTTP_201_CREATED,
                            detail="User is created")


@router.post("/token",
             response_model=Token,
             tags=['Auth'])
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(data.username, data.password)

    if not user or not user.is_created:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.name},
                                       expires_delta=access_token_expires)
    return Token(access_token=access_token,
                 token_type="bearer")
