from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from task_management_system import models, schemas
from task_management_system.models import Work, User, Task
from task_management_system.utils.idGenerator import generate_custom_id


def get_all_works(db: Session, current_user: User):
    if current_user.user_role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail='not authorized')
    db_data = db.query(Work).all()

    return db_data


def check_work(work: schemas.WorkCreate, db: Session):
    user = db.query(User).filter(User.userId == work.userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = db.query(Task).filter(Task.taskId == work.taskId,Task.assignedto == work.userId).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found for this user")
    
    # if task.userId != work.userId:
    #     raise HTTPException(status_code=403, detail="This task is not assigned to the user")

    try:
        time_spent = work.timeSpent
    except ValueError:
        raise HTTPException(status_code=400, detail="Time must be in format HH:MM:SS")

    work_id = generate_custom_id(db, Work, "workId", prefix="W")

    db_log = Work(
        workId=work_id,
        userId=work.userId,
        taskId=work.taskId,
        timeSpent=(work.timeSpent),
        workDate=work.workDate,
    )

    db.add(db_log)
    db.commit()
    return {"message": "Work completed", "time_spent": db_log.timeSpent}
