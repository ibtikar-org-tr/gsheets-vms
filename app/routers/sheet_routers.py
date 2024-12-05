from fastapi import APIRouter
from app.models import sheet_model
from app.handlers import sheet_handlers

router = APIRouter()

@router.get("/sheets/", response_model=list[sheet_model.Sheet])
def get_sheets():
    return sheet_handlers.get_sheets()

@router.post("/sheets/", response_model=sheet_model.Sheet)
def create_sheet(sheet: sheet_model.Sheet):
    return sheet_handlers.create_sheet(sheet)

@router.get("/sheets/{sheet_id}", response_model=sheet_model.Sheet)
def get_sheet_by_id(sheet_id: int):
    return sheet_handlers.get_sheet_by_id(sheet_id)

@router.put("/sheets/{sheet_id}", response_model=sheet_model.Sheet)
def update_sheet(sheet_id: int, sheet: sheet_model.Sheet):
    return sheet_handlers.update_sheet(sheet_id, sheet)