from app.db import db
from app.models import task_model

def get_all_tasks():
    return db.task_list

def create_new_task(task: task_model.task):
    db.task_list.append(task)
    return task

def get_task_by_id(task_id: int):
    for task in db.task_list:
        if task.id == task_id:
            return task
    return None

def update_task_by_id(task_id: int, task: task_model.task):
    for i, s in enumerate(db.task_list):
        if s.id == task_id:
            db.task_list[i] = task
            return task
    return None


