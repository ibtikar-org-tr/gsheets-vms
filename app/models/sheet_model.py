from pydantic import BaseModel, Field
import uuid

class Sheet(BaseModel):
    id: int = Field(default_factory=lambda: uuid.uuid4().int)
    sheetID: str

