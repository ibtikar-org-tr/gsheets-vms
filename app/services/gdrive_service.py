from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def add_permission_to_gdrive_folder(folder_link: str, mail: str):
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_API_JSON_PATH")

    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate with the service account
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    except Exception as e:
        print(f"Authentication failed (gsheet): {e}")
        return None
    
    # Connect to Google Drive
    drive_service = build('drive', 'v3', credentials=credentials)

    # Permission details
    new_permission = {
        'type': 'user',  # Can be 'user', 'group', 'domain', or 'anyone'
        'role': 'writer',  # Can be 'reader', 'commenter', or 'writer'
        'emailAddress': mail
    }

    try:
        # Add permission to the folder
        response = drive_service.permissions().create(
            fileId=folder_link_to_id(folder_link),
            body=new_permission,
            fields='id'
        ).execute()
        print(f"Permission granted: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    return response

def remove_permission_from_gdrive_folder(folder_link: str, mail: str):
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_API_JSON_PATH")

    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Authenticate with the service account
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    except Exception as e:
        print(f"Authentication failed (gsheet): {e}")
        return None
    
    # Connect to Google Drive
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        # Remove permission from the folder
        response = drive_service.permissions().delete(
            fileId=folder_link_to_id(folder_link),
            permissionId=mail
        ).execute()
        print(f"Permission removed: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    return response

def folder_link_to_id(folder_link: str) -> str:
    # Extract the folder ID from the link
    folder_id = folder_link.split('/')[-1].split('?')[0]
    return folder_id