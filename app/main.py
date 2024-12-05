from fastapi import FastAPI
from app.routers import sheet_routers, task_routers
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# Include routers
app.include_router(sheet_routers.router, prefix="/api/v1")
app.include_router(task_routers.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Volunteer Management System!"}
