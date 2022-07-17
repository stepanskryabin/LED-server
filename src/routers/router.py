from fastapi import APIRouter, Depends

from src.core.deps import check_auth_token
from src.routers import auth
from src.routers import admin_panel
from src.routers import home

api_router = APIRouter()

api_router.include_router(auth.router,
                          prefix="/auth")
api_router.include_router(admin_panel.router,
                          prefix="/admin",
                          dependencies=[Depends(check_auth_token)])
api_router.include_router(home.router)
