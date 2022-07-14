import heapq

from typing import Any


# class Singleton(type):
#     _instances = {}

#     def __call__(cls, *args: Any, **kwargs: Any) -> Any:
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


# class SessionQueue(metaclass=Singleton):
#     def __init__(self) -> None:
#         self.queue = []
#         heapq.heapify(self.queue)

#     async def pull(self,
#                    item: Any) -> None:
#         await heapq.heappush(self.queue, item)

#     async def push(self) -> Any:
#         return await heapq.heappop(self.queue)


async def check_auth_id(auth_id: str):
    pass
