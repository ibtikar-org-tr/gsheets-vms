from pydantic import BaseModel

class Sheet(BaseModel):
    id: int
    sheetName: str
    link: str
    managerID: int
