from app.db import db_connection
from app.models import activity_model
from sqlmodel import select

# repository functions
def get_all_activities():
    with db_connection.get_session() as session:
        activities = session.exec(select(activity_model.Task)).all()
    return activities

def get_activity_by_id(activity_id: str):
    with db_connection.get_session() as session:
        activity = session.get(activity_model.Activity, activity_id)
    return activity

def get_activity_by_manager_ID(manager_ID: str):
    with db_connection.get_session() as session:
        activity = session.exec(select(activity_model.Activity).where(activity_model.Activity.managerID == manager_ID)).first()
    return activity

def create_activity(activity: activity_model.Activity):
    with db_connection.get_session() as session:
        session.add(activity)
        session.commit()
        session.refresh(activity)
    return activity

def update_activity(activity: activity_model.Activity):
    with db_connection.get_session() as session:
        session.add(activity)
        session.commit()
        session.refresh(activity)
    return activity

def delete_activity(activity: activity_model.Activity):
    with db_connection.get_session() as session:
        session.delete(activity)
        session.commit()
    return activity

# service functions
def get_or_create_activity(managerID: str, managerName: str, projectName: str):
    activity = get_activity_by_manager_ID(managerID)
    if not activity:
        activity = activity_model.Activity(managerName=managerName, managerID=managerID, projectName=projectName)
        activity = create_activity(activity)
    return activity
