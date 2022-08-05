from fastapi import APIRouter

from src.routers import auth
from src.routers import admin_panel
from src.routers import home

api_router = APIRouter()

api_router.include_router(auth.router,
                          prefix="/auth")
api_router.include_router(admin_panel.router,
                          prefix="/admin")
api_router.include_router(home.router)
