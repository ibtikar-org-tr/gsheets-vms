from fastapi import FastAPI
from app.routers import sheets

app = FastAPI()

# Include routers
app.include_router(sheets.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Volunteer Management System!"}
