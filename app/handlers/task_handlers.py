from fastapi import HTTPException
from app.models import sheet_model
from app.services import gsheet_service
import logging

logger = logging.getLogger(__name__)

def check_tasks_from_sheet(sheet_link: str):
    try:
        sheet_id = gsheet_service.check_tasks_from_sheet(sheet_link)
        return sheet_id
    except Exception as e:
        logger.error(f"Error parsing sheet link {sheet_link}: {e}")
        raise HTTPException(status_code=400, detail="Invalid sheet link")
    