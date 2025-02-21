import os
import requests
from app.initializers import env

# def check_users_activity(list_of_users):
#     try:
#         list_of_usernames = []
#         for name, username in list_of_users:
#             list_of_usernames.append(username)
#         ACTIVITY_MS = os.getenv('ACTIVITY_MS')
#         payload = {'list_of_usernames': list_of_usernames}
#         response = requests.post(f"{ACTIVITY_MS}", json=payload)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Failed check_project_activity: {e}")

def check_user_activity(username):
    try:
        ACTIVITY_MS = env.ACTIVITY_MS
        response = requests.post(f"{ACTIVITY_MS}?username={username}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed check_project_activity: {e}")