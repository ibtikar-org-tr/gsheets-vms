from app.services import gdrive_service

def check_list_of_mails(folder_link: str, page_mails: list):
    will_be_added = []
    will_be_deleted = []
    existing_mails = []

    exising_permissions = gdrive_service.check_drive_folder_permission(folder_link)
    for permission in exising_permissions['permissions']:
        if permission['type'] == 'user' and not permission['role'] == 'owner':
            existing_mails.append(permission['emailAddress'])

    for mail in page_mails:
        if mail not in existing_mails:
            try:
                # gdrive_service.add_permission_to_gdrive_folder(folder_link, mail)
                will_be_added.append(mail)
            except Exception as e:
                print(f"An error occurred when adding {mail}: {e}")
    
    for mail in existing_mails:
        if mail not in page_mails:
            try:
                # gdrive_service.remove_permission_from_gdrive_folder(folder_link, mail)
                will_be_deleted.append(mail)
            except Exception as e:
                print(f"An error occurred when deleting {mail}: {e}")

    for mail in will_be_added:
        try:
            gdrive_service.add_permission_to_gdrive_folder(folder_link = folder_link, mail = mail)
            print(f"added: {mail}")
        except Exception as e:
            print(f"An error occurred when adding {mail}: {e}")

    for mail in will_be_deleted:
        try:
            gdrive_service.remove_permission_from_gdrive_folder(folder_link = folder_link, mail = mail)
            print(f"deleted: {will_be_deleted}")
        except Exception as e:
            print(f"An error occurred when deleting {mail}: {e}")


    print(f"added: {will_be_added}")
    print(f"deleted: {will_be_deleted}")


