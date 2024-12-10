# Makefile for running Uvicorn in the background

# Define the app command as a variable for easier reuse
UVICORN_CMD = nohup uvicorn app.main:app --reload --port 3001 &

# Target to start the Uvicorn app in the background
start:
	$(UVICORN_CMD)
	echo "Uvicorn app started on port 3001."

# Optional: Target to stop the Uvicorn app (find and kill the process)
stop:
	pkill -f 'uvicorn app.main:app'
	echo "Uvicorn app stopped."

# Optional: Target to restart the Uvicorn app
restart: stop start
