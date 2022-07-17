from fastapi import Header
from fastapi import HTTPException
from fastapi import status


async def check_auth_token(token: str = Header()) -> None:
    if token != 'token':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token header invalid")
