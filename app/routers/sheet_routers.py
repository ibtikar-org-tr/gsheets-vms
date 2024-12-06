from fastapi import APIRouter
from app.models import sheet_model
from app.handlers import sheet_handlers

router = APIRouter()

@router.get("/sheets/", response_model=list[sheet_model.Sheet])
def get_sheets():
    return sheet_handlers.get_sheets()

@router.post("/sheets/", response_model=sheet_model.Sheet)
def create_sheet(sheetID: str):
    return sheet_handlers.create_sheet(sheetID)

@router.get("/sheets/{sheet_id}", response_model=sheet_model.Sheet)
def get_sheet_by_id(sheet_id: str):
    return sheet_handlers.get_sheet_by_id(sheet_id)

@router.put("/sheets/{sheet_id}", response_model=sheet_model.Sheet)
def update_sheet(sheet_id: str, sheet: sheet_model.Sheet):
    return sheet_handlers.update_sheet(sheet_id, sheet)

@router.delete("/sheets/{sheet_id}", response_model=sheet_model.Sheet)
def delete_sheet(sheet_id: str):
    return sheet_handlers.delete_sheet(sheet_id)