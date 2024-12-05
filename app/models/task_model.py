from pydantic import BaseModel

class Task (BaseModel):
    id: int = None
    created_at: str
    updated_at: str
    sheetID: str # Sheet Model
    ownerID: int
    ownerName: str
    ownerEmail: str
    ownerPhone: str
    points: int
    status: str
    taskText: str
    priority: str
    dueDate: str
    notes: str
    completedDate: str = None
