from fastapi import APIRouter, HTTPException
from app.models import sheet_model
from app.services import sheet_service

router = APIRouter()

@router.get("/sheets/", response_model=list[sheet_model.Sheet])
def get_sheets():
    return sheet_service.get_all_sheets()

@router.post("/sheets/", response_model=sheet_model.Sheet)
def create_sheet(sheet: sheet_model.Sheet):
    return sheet_service.create_new_sheet(sheet)
