from pydantic import BaseModel, Field
import uuid

class Sheet(BaseModel):
    id: int = None
    sheetID: str

