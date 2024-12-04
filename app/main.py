from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Sheet(BaseModel):
    id: int
    name: str
    manager: str

sheets_db = []

@app.post("/sheets/", response_model=Sheet)
def create_sheet(sheet: Sheet):
    sheets_db.append(sheet)
    return sheet

@app.delete("/sheets/{sheet_id}", response_model=Sheet)
def delete_sheet(sheet_id: int):
    for sheet in sheets_db:
        if sheet.id == sheet_id:
            sheets_db.remove(sheet)
            return sheet
    raise HTTPException(status_code=404, detail="Sheet not found")

@app.put("/sheets/{sheet_id}", response_model=Sheet)
def update_sheet(sheet_id: int, updated_sheet: Sheet):
    for index, sheet in enumerate(sheets_db):
        if sheet.id == sheet_id:
            sheets_db[index] = updated_sheet
            return updated_sheet
    raise HTTPException(status_code=404, detail="Sheet not found")

@app.get("/sheets/", response_model=List[Sheet])
def get_sheets():
    return sheets_db

@app.get("/sheets/{sheet_id}", response_model=Sheet)
def get_sheet(sheet_id: int):
    for sheet in sheets_db:
        if sheet.id == sheet_id:
            return sheet
    raise HTTPException(status_code=404, detail="Sheet not found")