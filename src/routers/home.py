from fastapi import APIRouter
from fastapi import status
from fastapi import Request
from fastapi import HTTPException


router = APIRouter()


@router.get("/",
            status_code=status.HTTP_200_OK,
            responses={406: {"description": "Input limit > 100"}},
            tags=['Home'])
async def home_page(request: Request,
                    skip: int = 0,
                    limit: int = 10):
    if limit > 100:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Param=limit must be < 100, not {limit}")
    return {"result": f"Hello World skip={skip}, limit={limit}",
            "headers": request.headers,
            "cookies": request.cookies}
