# from fastapi import FastAPI,APIRouter,Depends,HTTPException
# from sqlalchemy.orm import Session
# from task_management_system.database import get_db
# from task_management_system import models, schemas
# from task_management_system.models import User, Work,UserRole
# from datetime import datetime
# from task_management_system.utils.idGenerator import generate_custom_id
# from task_management_system.utils.dependencies import get_current_user
# from task_management_system.schemas import WorkOut
 
# router = APIRouter()


# @router.get("/works",response_model=list[WorkOut])
# def get_all_works(db:Session = Depends(get_db),get_current_user:User = Depends(get_current_user)):
#     if get_current_user.user_role != UserRole.admin:
#         raise HTTPException(status_code=403, detail = 'not authorized')
#     return db.query(Work).all()


# @router.post("/work/check")
# def check_work(work: schemas.WorkCreate, db:Session = Depends(get_db),get_current_user: User = Depends(get_current_user)):
    
#     user= db.query(models.User).filter(models.User.userId==work.userId).first()
    
#     if not user:
#         raise HTTPException(status_code=404,detail="User not found")

#     task= db.query(models.Task).filter(models.Task.taskId==work.taskId).first()
#     # work_id = generate_custom_id(db,work,"workId",prefix="W")
    
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     # db_log = Work(
#     #     workId= generate_custom_id(
#     #         db,'Work', 'workId'

#     #     ),

#     try:
#         time_spent = datetime.strptime(work.timeSpent,"%H:%M:%S").time()
#     except ValueError:
#         raise HTTPException(status_code= 400, detail= "Time must be in format HH:MM:SS")

#     work_id = generate_custom_id(db,Work,"workId",prefix="W")
    
#     db_log= Work(
#         workId=work_id,
#         userId=work.userId,
#         taskId=work.taskId,
#         timeSpent = time_spent,
#         workDate=work.workDate,
#         # createdAt=work.createdAt
#     )

#     db.add(db_log)
#     db.commit()
#     return{"message":"Work completed in", "time_spent":db_log.timeSpent}

# # @router.delete("/work/{taskIdd}")
# # def delete_work(taskId: str, db:Session = Depends(get_db),get_current_user:User=Depends(get_current_user)):
# #     work= db.query(models.Work).filter(models.Work.taskId == taskId).first()
# #     if not work:
# #         raise HTTPException(status_code=404,detail="Work not found")
    
# #     db.delete(work)
# #     db.commit()
# #     return{"detail":"Work completed successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from task_management_system.database import get_db
from task_management_system.models import User
from task_management_system.schemas import WorkOut, WorkCreate
from task_management_system.utils.dependencies import get_current_user
from task_management_system.crud import crud_worklog

router = APIRouter()


@router.get("/works", response_model=list[WorkOut])
def get_all_works(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_worklog.get_all_works(db, current_user)


@router.post("/work/check")
def check_work(
    work: WorkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_worklog.check_work(work, db)
