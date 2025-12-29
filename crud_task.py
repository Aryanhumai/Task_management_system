from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from task_management_system import models, schemas
from task_management_system.utils.idGenerator import generate_custom_id
# from fastapi import Depends
# from task_management_system.dependencies import get_current_user, get_db


def get_all_tasks(db: Session):
    return db.query(models.Task).all()

def get_task_by_id(task_id: str, db: Session):
    task = db.query(models.Task).filter(models.Task.taskId == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# def create_task(task: schemas.TaskCreate, db: Session):
def create_task(
    task: schemas.TaskCreate,
    db: Session,
    current_user: models.User
):
   
    # assigned_by = db.query(models.User).filter(models.User.userId == task.assignedby).first()
    # if not assigned_by:
    #     raise HTTPException(status_code=404, detail="Assigned by user/admin doesn't exist")

    assigned_to = db.query(models.User).filter(models.User.userId == task.assignedto).first()
    if not assigned_to:
        raise HTTPException(status_code=404, detail="Assigned to user/admin doesn't exist")

    try:
        due_date = datetime.strptime(task.dueDate, "%Y:%m:%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Date must be in format YYYY:MM:DD")

    task_id = generate_custom_id(db, models.Task, 'taskId', prefix="T")
    db_task = models.Task(
        taskId=task_id,
        name=task.name,
        description=task.description,
        assignedby=current_user.userId,
        assignedto=task.assignedto,
        dueDate=due_date,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )
    db.add(db_task)
    db.commit()
    return {"message": "Task created", "taskId": db_task.taskId}

def update_task_details(task_id: str, task_update: schemas.TaskUpdateDetails, db: Session):
    db_task = get_task_by_id(task_id, db)

    update_data = task_update.dict(exclude_unset=True)
    PLACEHOLDER_VALUES = {"string"}

    cleaned_data = {
        k: v for k, v in update_data.items()
        if v is not None and str(v).strip() != "" and str(v).strip() not in PLACEHOLDER_VALUES
    }

    if not cleaned_data:
        raise HTTPException(status_code=400, detail="No valid fields provided for update.")

    if "assignedto" in cleaned_data:
        assigned_user = db.query(models.User).filter(models.User.userId == cleaned_data["assignedto"]).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    for key, value in cleaned_data.items():
        if key == "dueDate":
            value = datetime.strptime(value, "%Y:%m:%d")
        setattr(db_task, key, value)

    db_task.updatedAt = datetime.now()
    db.commit()

    return {"message": "Task updated successfully", "updated_fields": cleaned_data}

def update_task_status(task_id: str, status_update: schemas.TaskUpdateStatus, db: Session):
    db_task = get_task_by_id(task_id, db)
    db_task.status = status_update.status
    db_task.updatedAt = datetime.now()
    db.commit()
    return {"message": "Task updated successfully", "updated_status": db_task.status}

def delete_task(task_id: str, db: Session):
    task = db.query(models.Task).filter(models.Task.taskId == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
