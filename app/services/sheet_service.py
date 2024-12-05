from app.db import db
from app.models import sheet_model

def get_all_sheets():
    return db.sheet_list

def create_new_sheet(sheet: sheet_model.Sheet):
    db.sheet_list.append(sheet)
    return sheet

def get_sheet_by_id(sheet_id: int):
    for sheet in db.sheet_list:
        if sheet.id == sheet_id:
            return sheet
    return None

def update_sheet_by_id(sheet_id: int, sheet: sheet_model.Sheet):
    for i, s in enumerate(db.sheet_list):
        if s.id == sheet_id:
            db.sheet_list[i] = sheet
            return sheet
    return None