from pydantic import BaseModel, Field
from datetime import datetime

class Sheet(BaseModel):
    id: int = None
    sheetID: str
    modified_at: datetime
    modified_at: datetime

