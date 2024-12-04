from pydantic import BaseModel

class Sheet(BaseModel):
    id: int
    name: str
    manager: str
