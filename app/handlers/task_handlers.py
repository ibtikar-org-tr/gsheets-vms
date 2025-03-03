from fastapi import HTTPException
from app.services import task_service
import logging

logger = logging.getLogger(__name__)

async def get_all_tasks():
    return task_service.get_all_tasks()

async def check_tasks_from_sheet(sheet_id: str):
    if not sheet_id:
        raise HTTPException(status_code=400, detail="Sheet ID is required")
    try:
        task_service.check_tasks_from_sheet(sheet_id)
    except Exception as e:
        logger.error(f"Error parsing sheet id {sheet_id}: {e}")
        logger.error(f"Error occurred in file {e.__traceback__.tb_frame.f_code.co_filename}, function {e.__traceback__.tb_frame.f_code.co_name}, line {e.__traceback__.tb_lineno}")
        raise HTTPException(status_code=400, detail="Error parsing sheet id")

async def check_all_sheets():
    try:
        print("point1: task_handlers.check_all_sheets")
        task_service.check_all_sheets()
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        logger.error(f"Error occurred in file {e.__traceback__.tb_frame.f_code.co_filename}, function {e.__traceback__.tb_frame.f_code.co_name}, line {e.__traceback__.tb_lineno}")
        raise HTTPException(status_code=400, detail="Error parsing sheet ids")
    
async def run_task_15min_scheduler():
    try:
        task_service.run_task_15min_scheduler()
    except Exception as e:
        logger.error(f"Error running task scheduler: {e}")
        logger.error(f"Error occurred in file {e.__traceback__.tb_frame.f_code.co_filename}, function {e.__traceback__.tb_frame.f_code.co_name}, line {e.__traceback__.tb_lineno}")
        raise HTTPException(status_code=400, detail="Error running task scheduler")
    
async def start_scheduler():
    try:
        task_service.start_scheduler()
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        logger.error(f"Error occurred in file {e.__traceback__.tb_frame.f_code.co_filename}, function {e.__traceback__.tb_frame.f_code.co_name}, line {e.__traceback__.tb_lineno}")
        raise HTTPException(status_code=400, detail="Error starting scheduler")
    
async def stop_scheduler():
    try:
        task_service.stop_scheduler()
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
        logger.error(f"Error occurred in file {e.__traceback__.tb_frame.f_code.co_filename}, function {e.__traceback__.tb_frame.f_code.co_name}, line {e.__traceback__.tb_lineno}")
        raise HTTPException(status_code=400, detail="Error stopping scheduler")