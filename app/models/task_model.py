from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime
    updated_at: datetime
    last_sent: Optional[datetime] = None
    sheetID: str
    projectName: str
    pageID: int
    row_number: int
    ownerID: str
    ownerName: str
    ownerEmail: str
    ownerPhone: str
    managerName: str
    points: int
    status: str
    taskText: str
    priority: str
    dueDate: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    blocked_at: Optional[datetime] = None
    notes: str = None
    milestones: Optional[list[str]] = None
