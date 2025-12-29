from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from task_management_system import models, schemas
from task_management_system.database import get_db
from task_management_system.utils.dependencies import get_current_user
from task_management_system.models import User, UserRole
from task_management_system.schemas import TaskOut, TaskCreate
from task_management_system.crud import crud_task

router = APIRouter()

@router.get("/", response_model=list[schemas.TaskOut])
def get_all_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_role != UserRole.admin:
        raise HTTPException(status_code=403, detail='Not authorized')
    return crud_task.get_all_tasks(db)



@router.get("/task/{taskId}", response_model=schemas.TaskOut)
def view_task_by_id(
    taskId: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = crud_task.get_task_by_id(taskId, db)

    # ✅ ADMIN can view all tasks
    if current_user.user_role == UserRole.admin:
        return task

    # ✅ Normal users can view only assigned tasks
    if current_user.userId not in [task.assignedby, task.assignedto]:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")

    return task


@router.post("/create")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
     return crud_task.create_task(task, db, current_user)

@router.put("/tasks/task/updateAssignedby/{taskId}")
def update_task_details(taskId: str, task_update: schemas.TaskUpdateDetails, db: Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
    task = crud_task.get_task_by_id(taskId,db)
    if get_current_user.userId not in[task.assignedby]:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    return crud_task.update_task_details(taskId, task_update, db)



@router.put("/task/updateStatus/{taskId}")
def update_task_status(taskId: str, status_update: schemas.TaskUpdateStatus, db: Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
    task = crud_task.get_task_by_id(taskId,db)
    if get_current_user.userId not in[task.assignedto]:
        raise HTTPException(status_code=403,detail="Not authorized to update this task's status")
    return crud_task.update_task_details(taskId,status_update,db)
    
@router.delete("/task/{taskId}")
def delete_task(taskId: str, db: Session = Depends(get_db), get_current_user: User = Depends(get_current_user)):
    if get_current_user.user_role != UserRole.admin:
        raise HTTPException(status_code=403, detail='Not authorized')
    return crud_task.delete_task(taskId, db)
