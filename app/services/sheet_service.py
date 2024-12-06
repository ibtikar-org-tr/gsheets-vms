from app.models import sheet_model

from app.db import db_connection
from sqlmodel import select

def get_all_sheets():
    with db_connection.get_session() as session:
        sheets = session.exec(select(sheet_model.Sheet)).all()
    return sheets

def create_new_sheet(sheet: sheet_model.Sheet):
    with db_connection.get_session() as session:
        session.add(sheet)
        session.commit()
        session.refresh(sheet)
    return sheet

def get_sheet_by_id(sheet_id: int):
    with db_connection.get_session() as session:
        sheet = session.get(sheet_model.Sheet, sheet_id)
    return sheet


def update_sheet_by_id(sheet_id: int, sheet: sheet_model.Sheet):
    with db_connection.get_session() as session:
        existing_sheet = session.get(sheet_model.Sheet, sheet_id)
        if existing_sheet:
            for key, value in sheet.model_dump().items():
                setattr(existing_sheet, key, value)
            session.add(existing_sheet)
            session.commit()
            session.refresh(existing_sheet)
        return existing_sheet
