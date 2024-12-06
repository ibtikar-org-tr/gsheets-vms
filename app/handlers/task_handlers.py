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
        logger.error(f"Error parsing sheet ids: {e}")
        logger.error(f"Error occurred in file {e.__traceback__.tb_frame.f_code.co_filename}, function {e.__traceback__.tb_frame.f_code.co_name}, line {e.__traceback__.tb_lineno}")
        raise HTTPException(status_code=400, detail="Error parsing sheet ids")