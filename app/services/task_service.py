from app.db import db
from app.models import task_model
from app.services import gsheet_service
from app.services import send_service
from datetime import datetime

from app.db import db_connection
from sqlmodel import select

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

def get_task_by_id(task_id: int):
    with db_connection.get_session() as session:
        task = session.get(task_model.Task, task_id)
    return task

def search_task(sheetID: str, projectName: str, row_number: int):
    with db_connection.get_session() as session:
        task = session.exec(select(task_model.Task).where(task_model.Task.sheetID == sheetID, task_model.Task.projectName == projectName, task_model.Task.row_number == row_number)).first()
    return task

def update_task_by_id(task_id: int, task: task_model.Task):
    with db_connection.get_session() as session:
        existing_task = session.get(task_model.Task, task_id)
        if existing_task:
            for key, value in task.model_dump().items():
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
    # get the sheet
    sheet = gsheet_service.get_gsheet(sheet_id)
    if sheet is None:
        raise ValueError(f"Error parsing sheet id {sheet_id}: Sheet not found")

    # get the contacts page
    contacts = gsheet_service.get_contacts_page(sheet.worksheets())
    if contacts is None:
        raise ValueError(f"Error parsing sheet id {sheet_id}: Contacts not found")

    # iterate over the pages
    for page in sheet.worksheets():
        # skipping the contacts and imported pages
        if page.title.lower() not in ["contacts", "imported"]:
            # get all records from the page
            page_content = page.get_all_records()
            print(page.title)
            row_number = 1
            # iterate over the records
            for record in page_content:
                # prepare the task object
                contact = gsheet_service.get_specific_contact(contacts, record['owner'])
                created_at = datetime.strptime(record['Start date'], "%Y-%m-%d") if record['Start date'] else datetime.now()
                due_date = datetime.strptime(record['End date'], "%Y-%m-%d") if record['End date'] else None
                manager = contacts[0]
                sent = False

                # create a new task object
                task_obj = task_model.Task(
                    created_at=created_at,
                    updated_at=datetime.now(),
                    sheetID=sheet.id,
                    projectName=page.title,
                    pageID=page.id,
                    row_number=row_number,
                    ownerID=str(contact['number']),
                    ownerName=record['owner'],
                    ownerEmail=contact['mail'],
                    ownerPhone=str(contact['phone']),
                    managerName=manager['name1'],
                    points=record['points'],
                    status=record['Status'],
                    taskText=record['Task'],
                    priority=record['Priority'],
                    dueDate=due_date,
                    notes=record['Notes']
                )

                # check if the task is completed or blocked
                if task_obj.status.lower() == "completed":
                    task_obj.completed_at = datetime.now()
                    sent = True
                elif task_obj.status.lower() == "rejected":
                    task_obj.blocked_at = datetime.now()
                    sent = True
                
                # check if the task has missing data
                if not task_obj.ownerName or not task_obj.points or not task_obj.taskText or not task_obj.priority or not task_obj.dueDate:
                    if not sent: send_service.send_to_manager_missing_data(task_obj, manager)
                    sent = True


                # check if the task exists already
                existing_task = search_task(sheet.id, page.title, row_number)
                if existing_task:
                    # check if the task is late or needs reminders
                    if existing_task.last_sent:
                        if existing_task.last_sent > datetime.now() - 1:
                            sent = True
                        if task_obj.dueDate and task_obj.dueDate < datetime.now() and task_obj.last_sent < datetime.now() - 1:
                            if not sent: send_service.send_late_task(task_obj, manager); task_obj.last_sent = datetime.now(); sent = True
                        elif task_obj.dueDate and task_obj.dueDate > datetime.now() and task_obj.last_sent < datetime.now() - 1:
                            if not sent: send_service.send_updated_task(task_obj, manager); task_obj.last_sent = datetime.now(); sent = True
                    # check if the task is updated, and update it
                    if existing_task.ownerID != task_obj.ownerID:
                        if not sent: send_service.send_new_task(task_obj, manager); task_obj.last_sent = datetime.now(); sent = True
                        update_task_by_id(existing_task.id, task_obj)
                    elif existing_task.dueDate != task_obj.dueDate:
                        if not sent: send_service.send_updated_dueDate_task(existing_task, task_obj, manager); task_obj.last_sent = datetime.now(); sent = True
                        update_task_by_id(existing_task.id, task_obj)
                    if existing_task.status != task_obj.status or existing_task.points != task_obj.points or existing_task.taskText != task_obj.taskText or existing_task.priority != task_obj.priority or existing_task.notes != task_obj.notes:
                        update_task_by_id(existing_task.id, task_obj)
                # create the task if it doesn't exist
                else:
                    if not sent: send_service.send_new_task(task_obj, manager); task_obj.last_sent = datetime.now(); sent = True
                    create_new_task(task_obj)
                row_number += 1
        else:
            continue
    return "Tasks imported and sent successfully"

def check_all_sheets():
    for sheet in db.sheet_list:
        check_tasks_from_sheet(sheet.sheetID)
