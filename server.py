from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.db.worker import DBWorker
from src.settings import origins
from src.routers.router import api_router


app = FastAPI()

router = APIRouter()

db = DBWorker()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"])


app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    db.connect()
    db.create_record()


@app.on_event("shutdown")
def on_shutdown():
    db.disconnect()
