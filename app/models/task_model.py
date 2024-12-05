from pydantic import BaseModel

class Task (BaseModel):
    id: int
    created_at: str
    updated_at: str
    sheetID: int # Sheet Model
    ownerID: int
    ownerName: str 
    ownerEmail: str
    ownerPhone: str
    points: int
    status: str
    taskText: str
    priority: str
    dueDate: str
    completedDate: str
    milestones: list[str]
    notes: str
