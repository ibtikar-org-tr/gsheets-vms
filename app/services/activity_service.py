import os
import requests
from app.initializers import env
from app.services import send_service
from app.services import activity_repo
from datetime import datetime

def check_user_activity(username):
    try:
        ACTIVITY_MS = env.ACTIVITY_MS
        response = requests.post(f"{ACTIVITY_MS}?username={username}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed check_project_activity: {e}")

def check_and_report_project_activity(usernames_and_fullnames, manager_json):
    active_users = []
    inactive_users = []
    try:
        for username, fullname in usernames_and_fullnames.items():
            activity = check_user_activity(username)
            if activity:
                active_users.append(fullname)
            else:
                inactive_users.append(fullname)

        send_service.send_to_manager_daily_checkup(active_users, inactive_users, manager_json)

        # get activity and update last_reported
        activity_obj = activity_repo.get_activity_by_manager_ID(manager_json['number'])
        activity_obj.last_reported = datetime.now()
        activity_repo.update_activity(activity_obj)
    except Exception as e:
        print(f"Failed check_and_report_project_activity: {e}")

