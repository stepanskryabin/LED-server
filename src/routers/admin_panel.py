from fastapi import APIRouter, Depends
from fastapi import status
from fastapi import Response
from fastapi import Query

from src.core.deps import check_auth_token
from src.db.worker import DBWorker
from src.schemas.schemas import ErrorResponse
from src.schemas.schemas import UserResponse
from src.schemas.schemas import UserCreate


router = APIRouter()
db = DBWorker()


@router.get("/user",
            status_code=status.HTTP_200_OK,
            response_model=UserResponse,
            responses={404: {"model": ErrorResponse}},
            tags=['Admin panel'],
            dependencies=[Depends(check_auth_token)])
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
        return ErrorResponse(code=response.status_code,
                             detail="User not found")
    else:
        return result


@router.post("/user",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED,
             responses={500: {"model": ErrorResponse}},
             tags=['Admin panel'],
             dependencies=[Depends(check_auth_token)])
async def add_user(item: UserCreate,
                   response: Response):
    """
    Add new user.
    """

    try:
        db.add_user(item)
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponse(code=response.status_code,
                             detail="Unknow server error")
    else:
        return item
