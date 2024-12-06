from app.db import db
from app.models import task_model
from app.services import mail_service, task_service
from datetime import datetime

def send_new_task(task: task_model.Task, manager):
    text = f"""
    السّلام عليكم ورحمة الله وبركاته
    تمّ تعيين مهمّة جديدة لكم

    المهمّة: {task.taskText}
    الاستعجاليّة: {task.priority}
    آخر موعد للتّسليم: {task.dueDate}

    ملاحظات: {task.notes}

    المشروع: {task.projectName}
    مسؤول المشروع: {manager['name1']}
    رقم مسؤول المشروع: https://wa.me/{manager['phone']}
    رابط ملف المتابعة: https://docs.google.com/spreadsheets/d/{task.sheetID}/?gid={task.pageID}
    """

    mail_service.send_email(
        subject=f"مهمّة جديدة: {task.projectName}",
        body=text,
        to=task.ownerEmail
    )

    mail_service.send_sms(
        phone=task.ownerPhone,
        message=text
    )

    task.last_sent = datetime.now()
    task_service.update_task_by_search(task, task)

    return "Task sent successfully"

def send_updated_dueDate_task(old_task: task_model.Task, new_task: task_model.Task, manager):
    text = f"""
    السّلام عليكم
    تمّ تحديث تاريخ تسليم المهمّة التّالية ...
    
    المهمّة: {new_task.taskText}
    الاستعجاليّة: {new_task.priority}
    آخر موعد للتّسليم: {new_task.dueDate}
    كان سابقاً آخر موعد للتّسليم: {old_task.dueDate}
    
    ملاحظات: {new_task.notes}

    المشروع: {new_task.projectName}
    مسؤول المشروع: {manager['name1']}
    رقم مسؤول المشروع: https://wa.me/{manager['phone']}
    رابط ملف المتابعة: https://docs.google.com/spreadsheets/d/{new_task.sheetID}/?gid={new_task.pageID}
    """

    mail_service.send_email(
        subject=f"تحديث بخصوص المهمّة: {new_task.projectName}",
        body=text,
        to=new_task.ownerEmail
    )

    mail_service.send_sms(
        phone=new_task.ownerPhone,
        message=text
    )

    new_task.last_sent = datetime.now()
    task_service.update_task_by_search(old_task, new_task)

    return "Task sent successfully"

def send_late_task(task: task_model.Task, manager):
    text = f"""
    السّلام عليكم
    تذكير بشأن مهمذة متأخّرة !
    
    المهمّة: {task.taskText}
    الاستعجاليّة: {task.priority}
    آخر موعد للتّسليم: {task.dueDate}
    
    ملاحظات: {task.notes}

    المشروع: {task.projectName}
    مسؤول المشروع: {manager['name1']}
    رقم مسؤول المشروع: https://wa.me/{manager['phone']}
    رابط ملف المتابعة: https://docs.google.com/spreadsheets/d/{task.sheetID}/?gid={task.pageID}
    """

    mail_service.send_email(
        subject=f"مهمّة متأخّرة: {task.projectName}",
        body=text,
        to=task.ownerEmail
    )

    mail_service.send_sms(
        phone=task.ownerPhone,
        message=text
    )

    task.last_sent = datetime.now()
    task_service.update_task_by_search(task, task)

    return "Task sent successfully"