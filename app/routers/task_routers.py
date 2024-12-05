from fastapi import APIRouter
from app.handlers import task_handlers

router = APIRouter()

@router.get("/tasks")
async def get_all_tasks():
    return await task_handlers.get_all_tasks()

@router.post("/check_tasks")
async def check_tasks_from_sheet(id: str):
    return await task_handlers.check_tasks_from_sheet(id)

@router.get("/check_all_sheets")
async def check_all_sheets():
    return await task_handlers.check_all_sheets()

