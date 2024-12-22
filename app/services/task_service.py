from app.models import task_model
from app.db import db_connection
from app.services import gsheet_service
from app.services import sheet_service
from app.services import drive_service
from app.services import send_service
from app.services import formatting
from datetime import datetime, timedelta
import time
from sqlmodel import select
import pytz
from apscheduler.schedulers.background import BackgroundScheduler

def get_all_tasks():
    with db_connection.get_session() as session:
        tasks = session.exec(select(task_model.Task)).all()
    return tasks

def create_new_task(task: task_model.Task):
    with db_connection.get_session() as session:
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

def get_task_by_id(task_id: str):
    with db_connection.get_session() as session:
        task = session.get(task_model.Task, task_id)
    return task

def search_task(sheetID: str, projectName: str, row_number: int):
    with db_connection.get_session() as session:
        task = session.exec(select(task_model.Task).where(task_model.Task.sheetID == sheetID, task_model.Task.projectName == projectName, task_model.Task.row_number == row_number)).first()
    return task

def update_task_by_id(task_id: str, task: task_model.Task):
    with db_connection.get_session() as session:
        existing_task = session.get(task_model.Task, task_id)
        if existing_task:
            for key, value in task.model_dump().items():
                if key in ['updated_at', 'last_sent', 'last_reported'] and not value:
                    continue
                if key in ['created_at', 'completed_at', 'blocked_at'] and getattr(existing_task, key):
                    continue
                setattr(existing_task, key, value)
            session.add(existing_task)
            session.commit()
            session.refresh(existing_task)
        return existing_task

def update_task_by_search(old_task: task_model.Task, new_task: task_model.Task):
    task = search_task(old_task.sheetID, old_task.projectName, old_task.row_number)
    if task:
        return update_task_by_id(task.id, new_task)
    return None


def check_tasks_from_sheet(sheet_id: str):
    print("point5: task_service.check_tasks_from_sheet, start")
    # get the sheet
    sheet = gsheet_service.get_gsheet(sheet_id)
    if sheet is None:
        raise ValueError(f"Error parsing sheet id {sheet_id}: Sheet not found")

    # get the contacts page
    contacts = gsheet_service.get_contacts_page(sheet.worksheets())
    if contacts is None:
        raise ValueError(f"Error parsing sheet id {sheet_id}: Contacts not found")
    print("point9: task_service.check_tasks_from_sheet, contacts found")
    # iterate over the pages
    for page in sheet.worksheets():
        print("point10: task_service.check_tasks_from_sheet, iterate over pages")
        # skipping the contacts and imported pages
        if page.title.lower() not in ["contacts", "imported"]:
            # get all records from the page
            page_content = page.get_all_records()
            print(datetime.now(), "point11: task_service.check_tasks_from_sheet - found page with title:", page.title)
            # set the start row number to 1
            row_number = 1
            # set the associated folder link
            associated_folder_link = page_content[0]['Notes']
            print("associated_folder_link:", associated_folder_link, "with type:", type(associated_folder_link))
            # reset the project contacts' mail list
            page_contacts_mails= []
            # get the first contact as the manager
            manager = gsheet_service.get_specific_contact(contacts, page_content[0]['owner'])
            
            # iterate over the records
            for record in page_content:
                print("point12: task_service.check_tasks_from_sheet, iterate over records, row:", row_number)
                # prepare the task object
                try:
                    if record['owner'] and record['owner'].strip():
                        contact = gsheet_service.get_specific_contact(contacts, record['owner'])
                    else:
                        contact = {'number': '0', 'name1': 'Unknown', 'mail': 'Unknown', 'phone': 'Unknown'}
                except:
                    contact = {'number': '0', 'name1': 'Unknown', 'mail': 'Unknown', 'phone': 'Unknown'}

                try: created_at = formatting.strptime2(record['Start date']) if record['Start date'] else datetime.now()
                except: created_at = datetime.now()
                
                try: due_date = formatting.strptime2(record['Delivery date']) if record['Delivery date'] else None
                except: due_date = None
                
                send = True
                print("point13: task_service.check_tasks_from_sheet, task object preprepared")

                try:
                    # create a new task object
                    task_obj = task_model.Task(
                        created_at=created_at,
                        updated_at=datetime.now(),
                        sheetID=sheet.id,
                        projectName=str(page.title),
                        pageID=str(page.id),
                        row_number=row_number,
                        ownerID=str(contact['number']),
                        ownerName=record['owner'],
                        ownerEmail=contact['mail'],
                        ownerPhone=str(contact['phone']),
                        managerName=manager['name1'],
                        points=str(record['points']),
                        status=record['Status'],
                        taskText=record['Task'],
                        priority=record['Priority'],
                        dueDate=due_date,
                        notes=str(record['Notes'])
                    )
                except Exception as e:
                    print(f"at row {row_number}, Error creating task object: {e}")
                    continue
                
                print("point14: task_service.check_tasks_from_sheet, task object created")

                # add the contact's mail to the list
                if task_obj.ownerEmail:
                    if task_obj.ownerEmail not in page_contacts_mails:
                        page_contacts_mails.append(task_obj.ownerEmail)
                        print(f"point14.1: task_service.check_tasks_from_sheet, contact mail {task_obj.ownerEmail} added to list")

                # check if the task is completed or blocked
                if task_obj.status.lower() == "completed":
                    task_obj.completed_at = datetime.now()
                    send = False
                elif task_obj.status.lower() == "blocked":
                    task_obj.blocked_at = datetime.now()
                    send = False
                
                # check if the task exists already
                existing_task = search_task(sheet.id, page.title, row_number)

                # check if the task has missing data
                if any(not (value and (value.strip() if isinstance(value, str) else True)) for value in (task_obj.ownerName, task_obj.points, task_obj.taskText, task_obj.priority, task_obj.dueDate)):
                    if not existing_task:
                        if send: 
                            send_service.send_to_manager_missing_data(task_obj, manager)
                            task_obj.last_reported = datetime.now()
                            print(f"send missing data to manager, (if not existing_task), at row: {row_number}")
                    elif not existing_task.last_reported:
                        if send:
                            send_service.send_to_manager_missing_data(task_obj, manager)
                            task_obj.last_reported = datetime.now()
                            print(f"send missing data to manager, (elif not existing_task.last_reported), at row: {row_number}")
                    elif existing_task.last_reported and existing_task.last_reported < datetime.now() - timedelta(days=1):
                        if send:
                            send_service.send_to_manager_missing_data(task_obj, manager)
                            task_obj.last_reported = datetime.now()
                            print(f"send missing data to manager, (elif existing_task.last_reported and existing_task.last_reported < datetime.now() - timedelta(days=1)), at row: {row_number}")
                    send = False

                if existing_task:
                    # check if the task is late or needs reminders
                    if existing_task.last_sent and task_obj.dueDate:
                        if existing_task.last_sent > datetime.now() - timedelta(days=1):
                            send = False
                        if task_obj.dueDate and task_obj.dueDate < datetime.now() and existing_task.last_sent < datetime.now() - timedelta(days=1):
                            if send: send_service.send_late_task(task_obj, manager); task_obj.last_sent = datetime.now(); send = False
                        elif task_obj.dueDate and task_obj.dueDate > datetime.now() and existing_task.last_sent < datetime.now() - timedelta(days=1):
                            if send: send_service.send_reminder_task(task_obj, manager); task_obj.last_sent = datetime.now(); send = False
                    # check if the task has not been sent yet for some reason
                    elif not existing_task.last_sent:
                        if send: send_service.send_new_task(task_obj, manager); task_obj.last_sent = datetime.now(); send = False
                    # check if the task is updated, and send if necessary
                    if existing_task.ownerID != task_obj.ownerID:
                        if send: send_service.send_new_task(task_obj, manager); task_obj.last_sent = datetime.now(); send = False
                    elif existing_task.dueDate != task_obj.dueDate:
                        if send: send_service.send_updated_dueDate_task(existing_task, task_obj, manager); task_obj.last_sent = datetime.now(); send = False
                    # update anyways
                    update_task_by_id(existing_task.id, task_obj)
                # create the task if it doesn't exist
                else:
                    if send: send_service.send_new_task(task_obj, manager); task_obj.last_sent = datetime.now(); send = False
                    create_new_task(task_obj)

                print("point15: task_service.check_tasks_from_sheet, task processed at row:", row_number)
                row_number += 1

            # check the contacts' mails
            if page_contacts_mails:
                drive_service.check_list_of_mails(folder_link = associated_folder_link, page_mails = page_contacts_mails)
                print("point16: task_service.check_tasks_from_sheet, page contacts mails checked")
            else:
                print("point16x: task_service.check_tasks_from_sheet, no contacts mails found") 
        else:
            continue
    return "Tasks imported and sent successfully"


def check_all_sheets():
    print("point2: task_service.check_all_sheets, start")
    sheets = sheet_service.get_all_sheets()
    for sheet in sheets:
        print("point4: task_service.check_all_sheets, iterate over sheets")
        check_tasks_from_sheet(sheet.sheetID)

def check_all_sheets_at_work_hours():
    istanbul_tz = pytz.timezone('Europe/Istanbul')
    if 8 <= datetime.now(istanbul_tz).hour < 22:
        print("Running check_all_sheets_at_work_hours... at", datetime.now())
        check_all_sheets()
    else:
        print("Outside of working hours. timestamp is", datetime.now())

def run_task_15min_scheduler():
    istanbul_tz = pytz.timezone('Europe/Istanbul')
    while True:
        try:
            now = datetime.now(istanbul_tz)
            if now.hour >= 8 and now.hour < 22:
                print("Running run_task_15min_scheduler... at", datetime.now())
                check_all_sheets()
                print("Completed run_task_15min_scheduler. at", datetime.now())
            else:
                print("Outside of working hours. timestamp is", datetime.now())
        except Exception as e:
            print("Error running run_task_15min_scheduler:", e)
        time.sleep(15 * 60)

scheduler = BackgroundScheduler()

def start_scheduler():
    # Run the task immediately
    try:
        check_all_sheets_at_work_hours()
    except Exception as e:
        print("Error running check_all_sheets:", e)

    # Schedule the task to run every 15 minutes
    scheduler.add_job(check_all_sheets_at_work_hours, 'interval', minutes=15)
    scheduler.start()
    print("Scheduler started at", datetime.now())

def stop_scheduler():
    scheduler.shutdown()
    print("Scheduler stopped at", datetime.now())