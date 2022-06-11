from pydantic import BaseModel


class SupportForm(BaseModel):
    user_name: str
    date_time: int
    time_zone: str
    email: str
    message: str
    importance: int
