from google.oauth2 import service_account
from googleapiclient.discovery import build
import os


def add_mail_to_ggroup(member_mail: str, group_mail: str):
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_API_JSON_PATH")

    SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']

    # Authenticate with the service account
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    except Exception as e:
        print(f"Authentication failed (gsheet): {e}")
        return None

    # Connect to Google Admin SDK
    service = build('admin', 'directory_v1', credentials=credentials)

    # Specify the group email and the new member details
    new_member = {
        'email': member_mail,
        'role': 'MEMBER'  # Options: MEMBER, MANAGER, OWNER
    }

    # Add the member to the group
    try:
        # Check if the member is already in the group
        result = service.members().get(groupKey=group_mail, memberKey=member_mail).execute()
        print(f"Member {member_mail} is already in the group.")
    except Exception as e:
        # If the member is not found, add them to the group
        if 'Member not found' in str(e):
            result = service.members().insert(groupKey=group_mail, body=new_member).execute()
            print(f"Added member: {result}")
        else:
            print(f"An error occurred: {e}")
            return None

    return result

# def add_mail_list_to_ggroup(mails_list: list, group_mail: str):
#     for mail in mails_list:
#         if mail:
#             add_mail_to_ggroup(mail, group_mail)
#         else:
#             print("Empty mail, skipping...", mail)
#             continue