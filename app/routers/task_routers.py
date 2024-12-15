from fastapi import APIRouter
from app.handlers import task_handlers

router = APIRouter()

@router.get("/tasks")
async def get_all_tasks():
    return await task_handlers.get_all_tasks()

@router.post("/check_sheet")
async def check_tasks_from_sheet(id: str):
    await task_handlers.check_tasks_from_sheet(id)
    return {"message": "Tasks checked successfully"}

@router.post("/check_all_sheets")
async def check_all_sheets():
    await task_handlers.check_all_sheets()
    return {"message": "all sheets' Tasks checked successfully"}

@router.post("/run_task_15min_scheduler")
async def run_task_15min_scheduler():
    await task_handlers.run_task_15min_scheduler()
    return {"message": "Background task started to check all sheets every 15 minutes"}

@router.post("/start-scheduler")
async def start_scheduler_endpoint():
    await task_handlers.start_scheduler()
    return {"message": "Scheduler started."}

@router.post("/stop-scheduler")
async def stop_scheduler_endpoint():
    await task_handlers.stop_scheduler()
    return {"message": "Scheduler stopped."}