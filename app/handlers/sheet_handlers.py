from fastapi import HTTPException
from app.models import sheet_model
from app.services import sheet_service
import logging

logger = logging.getLogger(__name__)

def get_sheets():
    return sheet_service.get_all_sheets()

def create_sheet(sheet: sheet_model.Sheet):
    return sheet_service.create_new_sheet(sheet)

def get_sheet_by_id(sheet_id: int):
    try:
        sheet = sheet_service.get_sheet_by_id(sheet_id)
        if sheet is None:
            logger.warning(f"Sheet with id {sheet_id} not found")
            raise HTTPException(status_code=404, detail="Sheet not found")
        return sheet
    except Exception as e:
        logger.error(f"Error retrieving sheet with id {sheet_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def update_sheet(sheet_id: int, sheet: sheet_model.Sheet):
    try:
        updated_sheet = sheet_service.update_sheet_by_id(sheet_id, sheet)
        if updated_sheet is None:
            logger.warning(f"Sheet with id {sheet_id} not found")
            raise HTTPException(status_code=404, detail="Sheet not found")
        return updated_sheet
    except Exception as e:
        logger.error(f"Error updating sheet with id {sheet_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")