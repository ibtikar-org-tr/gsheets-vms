from app.db import db_connection
from app.models import manager_model
from sqlmodel import select

# repository functions
def get_all_managers():
    with db_connection.get_session() as session:
        managers = session.exec(select(manager_model.Task)).all()
    return managers

def get_manager_by_id(manager_id: str):
    with db_connection.get_session() as session:
        manager = session.get(manager_model.Manager, manager_id)
    return manager

def get_manager_by_manager_ID(manager_ID: str):
    with db_connection.get_session() as session:
        manager = session.exec(select(manager_model.Manager).where(manager_model.Manager.managerID == manager_ID)).first()
    return manager

def create_manager(manager: manager_model.Manager):
    with db_connection.get_session() as session:
        session.add(manager)
        session.commit()
        session.refresh(manager)
    return manager

def update_manager(manager: manager_model.Manager):
    with db_connection.get_session() as session:
        session.add(manager)
        session.commit()
        session.refresh(manager)
    return manager

def delete_manager(manager: manager_model.Manager):
    with db_connection.get_session() as session:
        session.delete(manager)
        session.commit()
    return manager

# service functions
def get_or_create_manager(managerID: str, managerName: str):
    manager = get_manager_by_manager_ID(managerID)
    if not manager:
        manager = manager_model.Manager(managerName=managerName, managerID=managerID)
        manager = create_manager(manager)
    return manager
