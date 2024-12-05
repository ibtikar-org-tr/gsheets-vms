from fastapi import HTTPException
from app.models import sheet_model
from app.services import task_service
import logging

logger = logging.getLogger(__name__)

def get_all_tasks():
    return task_service.get_all_tasks()

def check_tasks_from_sheet(sheet_id: str):
    try:
        task_service.check_tasks_from_sheet(sheet_id)
    except Exception as e:
        logger.error(f"Error parsing sheet link {sheet_id}: {e}")
        raise HTTPException(status_code=400, detail="Invalid sheet id")
    

def check_all_sheets():
    try:
        task_service.check_all_sheets()
    except Exception as e:
        logger.error(f"Error parsing sheet ids: {e}")
        raise HTTPException(status_code=400, detail="Invalid sheet id")