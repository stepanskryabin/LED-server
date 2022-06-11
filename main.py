from fastapi import FastAPI

from src.settings import ABOUT
from src.help_desk.views import get_support_page
from src.help_desk.views import post_support_page


app = FastAPI(description=ABOUT["description"],
              version=ABOUT["version"],
              contact=ABOUT["contact"])


@app.get("/")
async def get_root(skip: int = 0, limit: int = 10):
    if limit > 100:
        return "Error!"
    return f"Hello World skip={skip}, limit={limit}"


@app.put("/")
async def put_root():
    return None


@app.post("/")
async def post_root():
    return None


@app.get("/support/{item}")
async def get_support(item: int):
    return await get_support_page(_input=item)


@app.put("/support/{item}")
async def put_support(item):
    return await post_support_page(_input=item)
