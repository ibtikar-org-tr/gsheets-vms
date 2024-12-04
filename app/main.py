from fastapi import FastAPI
from app.routers import sheet_routers

app = FastAPI()

# Include routers
app.include_router(sheet_routers.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Volunteer Management System!"}
