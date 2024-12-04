from pydantic import BaseModel

class Volunteer(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: str
    roleID: int
    sheetIDs: list[int]
    created_at: str
    updated_at: str