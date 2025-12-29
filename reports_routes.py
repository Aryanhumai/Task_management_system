# routers/reports_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from task_management_system.database import get_db
from task_management_system.models import User
from task_management_system.schemas import TaskOut
from task_management_system.utils.dependencies import get_current_user
from task_management_system.crud import crud_reports

router = APIRouter()


@router.get("/view_tasks", response_model=list[TaskOut])
def get_all_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_reports.get_all_tasks(db, current_user)


@router.get("/view_tasks/assignedby/{userId}", response_model=list[TaskOut])
def get_tasks_assigned_by_user(
    userId: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_reports.get_tasks_assigned_by_user(userId, db)


@router.get("/view_tasks/assignedto/{userId}", response_model=list[TaskOut])
def get_tasks_assigned_to_user(
    userId: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_reports.get_tasks_assigned_to_user(userId, db)
