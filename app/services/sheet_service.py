from app.db import sheets_db
from app.models import sheet_model

def get_all_sheets():
    return sheets_db.db_list

def create_new_sheet(sheet: sheet_model.Sheet):
    sheets_db.db_list.append(sheet)
    return sheet
