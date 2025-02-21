import os
import requests
from app.initializers import env
from app.models import Manager
from app.services import send_service
from app.services import manager_service
from datetime import datetime

def check_user_activity(username):
    try:
        ACTIVITY_MS = env.ACTIVITY_MS
        response = requests.post(f"{ACTIVITY_MS}?username={username}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed check_project_activity: {e}")

def check_project_activity(usernames, manager):
    active_users = []
    inactive_users = []

    for username in usernames:
        activity = check_user_activity(username)
        if activity:
            active_users.append(username)
        else:
            inactive_users.append(username)

    send_service.send_to_manager_daily_checkup(active_users, inactive_users, manager)

    # update last_reported for manager
    manager.last_reported = datetime.now()
    manager_service.update_manager(manager)

