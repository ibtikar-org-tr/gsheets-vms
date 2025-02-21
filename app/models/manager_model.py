from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Manager(SQLModel, table=True): # Daily checkup for the manager
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime
    updated_at: datetime
    last_reported: Optional[datetime] = None
    managerName: str
    managerID: str