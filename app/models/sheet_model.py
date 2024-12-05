from pydantic import BaseModel

class Sheet(BaseModel):
    id: int
    sheetID: str

