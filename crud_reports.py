# crud/crud_reports.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from task_management_system import models
from task_management_system.models import User, Task, UserRole


def get_all_tasks(db: Session, current_user: User):
    if current_user.user_role != UserRole.admin:
        raise HTTPException(status_code=403, detail='Not authorized')
    return db.query(Task).all()


def get_tasks_assigned_by_user(user_id: str, db: Session):
    tasks = db.query(models.Task).filter(models.Task.assignedby == user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")
    return tasks


def get_tasks_assigned_to_user(user_id: str, db: Session):
    tasks = db.query(models.Task).filter(models.Task.assignedto == user_id).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found by this user")
    return tasks
