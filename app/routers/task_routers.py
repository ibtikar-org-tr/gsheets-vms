from fastapi import APIRouter
from app.handlers import task_handlers

router = APIRouter()

@router.post("/check_tasks")
async def check_tasks_from_sheet(id: str):
    return await task_handlers.check_tasks_from_sheet(id)