from pydantic import BaseModel

class Sheet(BaseModel):
    id: int
    sheetName: str
    sheetLink: str
    managerID: int

