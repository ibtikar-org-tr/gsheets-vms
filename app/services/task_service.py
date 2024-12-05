from app.db import db
from app.models import task_model
from app.services import gsheet_service
from datetime import datetime

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

def update_task_by_id(task_id: int, task: task_model.Task):
    for i, s in enumerate(db.task_list):
        if s.id == task_id:
            db.task_list[i] = task
            return task
    return None

def check_tasks_from_sheet(sheet_id: str):
    sheet = gsheet_service.get_gsheet(sheet_id)
    contacts = gsheet_service.get_contacts_page(sheet.worksheets())
    for page in sheet.worksheets():
        if page.title not in ["contacts", "imported"]:
            page_content = page.get_all_records()
            print(page.title)
            # print(page_content)
            for record in page_content:
                contact = gsheet_service.get_specific_contact(contacts, record['owner'])
                created_at = datetime.strptime(record['Start date'], "%Y-%m-%d") if record['Start date'] else datetime.now()
                due_date = datetime.strptime(record['End date'], "%Y-%m-%d") if record['End date'] != "" else None

                record_obj = task_model.Task(
                    # id=record['id'],
                    created_at=created_at,
                    updated_at=datetime.now(),
                    sheetID=sheet.id,
                    ownerID=contact['number'],
                    ownerName=record['owner'],
                    ownerEmail=contact['mail'],
                    ownerPhone=str(contact['phone']),
                    points=record['points'],
                    status=record['Status'],
                    taskText=record['Task'],
                    priority=record['Priority'],
                    dueDate=due_date,
                    # completedDate=record['completedDate'],
                    notes=record['Notes']
                )
                create_new_task(record_obj)
        else:
            continue
    return "Tasks imported successfully"

def check_all_sheets():
    for sheet in db.sheet_list:
        check_tasks_from_sheet(sheet.sheetID)