from app.db import db
from app.models import task_model
from app.services import gsheet_service
from app.services import send_service
from datetime import datetime
from typing import Optional

def get_all_tasks():
    return db.task_list

def create_new_task(task: task_model.Task):
    db.task_list.append(task)
    return task

def get_task_by_id(task_id: int):
    for task in db.task_list:
        if task.id == task_id:
            return task
    return None

def search_task(sheetID: str, projectName: str, row_number: int):
    for task in db.task_list:
        if task.sheetID == sheetID and task.projectName == projectName and task.row_number == row_number:
            return task
    return None

def update_task_by_id(task_id: int, task: task_model.Task):
    for i, s in enumerate(db.task_list):
        if s.id == task_id:
            db.task_list[i] = task
            return task
    return None

def update_task_by_search(old_task: task_model.Task, new_task: task_model.Task):
    task = search_task(old_task.sheetID, old_task.projectName, old_task.row_number)
    for i, s in enumerate(db.task_list):
        if s.id == task.id:
            db.task_list[i] = new_task
            return task
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
