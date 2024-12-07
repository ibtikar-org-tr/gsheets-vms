# Define variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/Scripts/python
PIP = $(VENV_DIR)/Scripts/pip
UVICORN = $(VENV_DIR)/Scripts/uvicorn
ALEMBIC = $(VENV_DIR)/Scripts/alembic

# Detect the operating system
ifeq ($(OS),Windows_NT)
    PYTHON = $(VENV_DIR)\Scripts\python.exe
    PIP = $(VENV_DIR)\Scripts\pip.exe
    UVICORN = $(VENV_DIR)\Scripts\uvicorn.exe
    ALEMBIC = $(VENV_DIR)\Scripts\alembic.exe
    RM = del /Q
    RMDIR = rmdir /S /Q
else
    PYTHON = $(VENV_DIR)/bin/python
    PIP = $(VENV_DIR)/bin/pip
    UVICORN = $(VENV_DIR)/bin/uvicorn
    ALEMBIC = $(VENV_DIR)/bin/alembic
    RM = rm -f
    RMDIR = rm -rf
endif

# Default target
.PHONY: help
help:
    @echo "Usage:"
    @echo "  make setup          - Set up the virtual environment and install dependencies"
    @echo "  make migrate        - Run database migrations"
    @echo "  make run            - Start the FastAPI server"
    @echo "  make clean          - Clean up the project"

# Set up the virtual environment and install dependencies
.PHONY: setup
setup:
    @echo "Creating virtual environment..."
    python -m venv $(VENV_DIR)
    @echo "Activating virtual environment and installing dependencies..."
    $(PIP) install -r requirements.txt

# Run database migrations
.PHONY: migrate
migrate:
    @echo "Running database migrations..."
    $(ALEMBIC) upgrade head

# Start the FastAPI server
.PHONY: run
run:
    @echo "Starting the FastAPI server..."
    $(UVICORN) app.main:app --reload --port 3001

# Clean up the project
.PHONY: clean
clean:
    @echo "Cleaning up the project..."
    $(RMDIR) $(VENV_DIR)
    find . -type d -name "__pycache__" -exec $(RMDIR) {} +
    find . -type d -name "*.egg-info" -exec $(RMDIR) {} +
    find . -type d -name "*.pytest_cache" -exec $(RMDIR) {} +