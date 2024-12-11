from app.models import task_model
from app.services import mail_service, task_service
from datetime import datetime

# SEND to VOlUNTEER ------------------------------------------------
def send_new_task(task: task_model.Task, manager):
    text = f"""
    السّلام عليكم ورحمة الله وبركاته
    تمّ تعيين مهمّة جديدة لكم

    المهمّة: *{task.taskText}*
    الاستعجاليّة: {task.priority}
    آخر موعد للتّسليم: *{task.dueDate.strftime("%Y-%m-%d") if task.dueDate else "N/A"}*

    ملاحظات: {task.notes}

    المشروع: {task.projectName}
    مسؤول المشروع: {manager['name1']}
    رقم مسؤول المشروع: wa.me/{manager['phone']}

    رابط ملف المتابعة: https://docs.google.com/spreadsheets/d/{task.sheetID}/?gid={task.pageID}
    """

    mail_service.send_email(
        to=task.ownerEmail,
        subject=f"مهمّة جديدة: {task.projectName}",
        message=text,
    )

    mail_service.send_sms(
        phone=task.ownerPhone,
        message=text
    )

    return "send_new_task sent successfully"

def send_updated_dueDate_task(old_task: task_model.Task, new_task: task_model.Task, manager):
    text = f"""
    السّلام عليكم
    تمّ تحديث تاريخ تسليم المهمّة التّالية ...
    
    المهمّة: *{new_task.taskText}*
    الاستعجاليّة: {new_task.priority}
    آخر موعد للتّسليم: *{new_task.dueDate.strftime("%Y-%m-%d") if new_task.dueDate else "N/A"}*
    كان سابقاً آخر موعد للتّسليم: {old_task.dueDate.strftime("%Y-%m-%d") if old_task.dueDate else "N/A"}
    
    ملاحظات: {new_task.notes}

    المشروع: {new_task.projectName}
    مسؤول المشروع: {manager['name1']}
    رقم مسؤول المشروع: wa.me/{manager['phone']}

    رابط ملف المتابعة: https://docs.google.com/spreadsheets/d/{new_task.sheetID}/?gid={new_task.pageID}
    """

    mail_service.send_email(
        to=new_task.ownerEmail,
        subject=f"تحديث بخصوص المهمّة: {new_task.projectName}",
        message=text
    )

    mail_service.send_sms(
        phone=new_task.ownerPhone,
        message=text
    )

    return "send_updated_dueDate_task sent successfully"

def send_late_task(task: task_model.Task, manager):
    text = f"""
    السّلام عليكم
    تذكير بشأن مهمّة متأخّرة !
    
    المهمّة: *{task.taskText}*
    الاستعجاليّة: {task.priority}
    آخر موعد للتّسليم كان: *{task.dueDate.strftime("%Y-%m-%d") if task.dueDate else "N/A"}*
    
    ملاحظات: {task.notes}

    المشروع: {task.projectName}
    مسؤول المشروع: {manager['name1']}
    رقم مسؤول المشروع: wa.me/{manager['phone']}

    رابط ملف المتابعة: https://docs.google.com/spreadsheets/d/{task.sheetID}/?gid={task.pageID}
    """

    mail_service.send_email(
        to=task.ownerEmail,
        subject=f"مهمّة متأخّرة: {task.projectName}",
        message=text
    )

    mail_service.send_sms(
        phone=task.ownerPhone,
        message=text
    )

    return "send_late_task sent successfully"

# SEND to MANAGER ------------------------------------------------
def send_to_manager_missing_data(task: task_model.Task, manager):
    text = f"""
    السّلام عليكم
    تحتاج المهمّة التّالية إلى تحديثات
    
    المهمّة: *{task.taskText}*
    الاستعجاليّة: {task.priority}
    آخر موعد للتّسليم: *{task.dueDate.strftime("%Y-%m-%d") if task.dueDate else "N/A"}*
    
    ملاحظات: {task.notes}

    المشروع: {task.projectName}
    مسؤول المهمّة: {task.ownerName}
    رقم مسؤول المهمّة: wa.me/{task.ownerPhone}

    رابط ملف المتابعة: https://docs.google.com/spreadsheets/d/{task.sheetID}/?gid={task.pageID}
    """

    mail_service.send_email(
        to=manager['mail'],
        subject=f"معلومات ناقصة بخصوص المهمّة: {task.projectName}",
        message=text
    )

    mail_service.send_sms(
        phone=manager['phone'],
        message=text
    )

    return "send_to_manager_missing_data sent successfully"