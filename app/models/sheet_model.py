from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Sheet(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    sheetID: str
    created_at: datetime = datetime.now()

