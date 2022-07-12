from mimetypes import init
from typing import Any


class Singleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AuthSession(metaclass=Singleton):
    def __init__(self) -> None:
        self.session = []


async def check_auth_id(auth_id: str):
    pass
