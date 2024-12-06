import gspread
from google.oauth2.service_account import Credentials
import os
import time
from app.services import task_service
from app.models import task_model

# Define the scope for Google Sheets and Drive API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]

def get_gsheet(sheet_id: str):
    print("point6: gsheet_service.get_gsheet, start")

    # Path to your service account key file
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_API_JSON_PATH")
    print("point7: gsheet_service.get_gsheet, GOOGLE_API_JSON_PATH")

    # Authenticate with the service account
    try:
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
    except Exception as e:
        print(f"Authentication failed (gsheet): {e}")
        return None

    # Connect to Google Sheets
    client = gspread.authorize(credentials)

    # Open the spreadsheet using its ID
    sheet = client.open_by_key(sheet_id)
    
    print("point8: gsheet_service.get_gsheet, end")
    return sheet

def get_contacts_page(sheet):
    for page in sheet:
        if page.title.lower() == "contacts":
            contacts_page = page.get_all_records()
            # contacts_page_id = page.id
        else:
            continue
    return contacts_page

def get_specific_contact(contacts_page, contact_name):
# search for a contact details by name
    for contact in contacts_page:
        if contact['name1'] == contact_name:
            # print("name1: ", contact['name1'])
            # print("number: ", contact['number'])
            # print("name2: ", contact['name2'])
            # print("phone: ", contact['phone'])
            # print("mail: ", contact['mail'])
            # print("sex: ", contact['sex'])
            # print("mission-ar: ", contact['mission-ar'])
            # print("total points: ", contact['total points'])
            # print("rank: ", contact['rank'])
            # print("global Rank: ", contact['global Rank'])
            return contact


