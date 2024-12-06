from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    created_at: datetime
    updated_at: datetime
    last_sent: Optional[datetime] = None
    sheetID: str
    projectName: str
    pageID: str
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
