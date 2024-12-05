from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: datetime
    last_login: datetime

