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
        print(f"Permission granted for {mail} on {folder_link}: {response}")
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
        print(f"Permission removed for {mail} on {folder_link}: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    return response

def check_drive_folder_permission(folder_link: str):
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
        # Get the permission details of the folder
        response = drive_service.permissions().list(
            fileId=folder_link_to_id(folder_link),
            fields='permissions(emailAddress,type,role)'
        ).execute()
        print(f"Folder permissions: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    return response

def folder_link_to_id(folder_link: str) -> str:
    # Extract the folder ID from the link
    folder_id = folder_link.split('/')[-1]
    folder_id = folder_id.split('?')[0]

    return folder_id
