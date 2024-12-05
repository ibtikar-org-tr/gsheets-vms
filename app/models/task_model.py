from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task (BaseModel):
    id: int = None
    created_at: datetime
    updated_at: datetime
    sheetID: str # Sheet Model
    ownerID: int
    ownerName: str
    ownerEmail: str
    ownerPhone: str
    points: int
    status: str
    taskText: str
    priority: str
    dueDate: datetime = None
    notes: str
    completedDate: str = None
