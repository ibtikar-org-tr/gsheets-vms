from app.db import sheets_db
from app.models import sheet_model

def get_all_sheets():
    return sheets_db.db_list

def create_new_sheet(sheet: sheet_model.Sheet):
    sheets_db.db_list.append(sheet)
    return sheet

def get_sheet_by_id(sheet_id: int):
    for sheet in sheets_db.db_list:
        if sheet.id == sheet_id:
            return sheet
    return None

def update_sheet_by_id(sheet_id: int, sheet: sheet_model.Sheet):
    for i, s in enumerate(sheets_db.db_list):
        if s.id == sheet_id:
            sheets_db.db_list[i] = sheet
            return sheet
    return None