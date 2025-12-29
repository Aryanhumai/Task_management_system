# from fastapi import APIRouter, Depends,HTTPException
# from sqlalchemy import or_
# from sqlalchemy.orm import Session
# from task_management_system.database import SessionLocal, get_db
# from task_management_system.models import User,UserStatus, Task,Work, Logged, UserRole
# from datetime import datetime
# from task_management_system import schemas,models
# from uuid import uuid4
# from typing import List
# from task_management_system.schemas import UserOut
# from task_management_system.auth import hash_password
# from task_management_system import auth
# from task_management_system.utils.dependencies import get_current_user
# from task_management_system.utils.idGenerator import generate_custom_id


# router = APIRouter()

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# @router.get("/users", response_model=List[UserOut])
# def get_all_users(db: Session = Depends(get_db)):
#     return db.query(User).all()

# @router.post("/create-user")
# def create_user(
#     user: schemas.UserCreate,
#     db: Session = Depends(get_db),
#     get_current_user: User = Depends(get_current_user)
# ):
#     existing_mobile = db.query(User).filter(User.mobile == user.mobile).first()

#     if get_current_user.user_role != UserRole.admin:
#         raise HTTPException(status_code=403, detail = 'not authorized')

#     if existing_mobile:
#         raise HTTPException(
#             status_code=400,
#             detail="Mobile number already exists. Please enter a correct number."
#         )
    
#     existing_email = db.query(User).filter(User.email == user.email).first()
#     if existing_email:
#         raise HTTPException(
#             status_code=400,
#             detail="Email already registered. Please use a different email."
#         )

#     custom_id = generate_custom_id( db,User,'userId',prefix="U")
#     hashed_pwd = hash_password(user.password)
#     db_user = User(
#         userId=custom_id,  
#         name=user.name,
#         password=hashed_pwd,
#         mobile=user.mobile,
#         email=user.email,
#         # status=user.status,
#         # user_role=user.user_role,
#         createdAt=datetime.now(),
#         updatedAt=datetime.now()
#     )
#     db.add(db_user)
#     db.commit()
#     return {"message": "User created", "userId": db_user.userId}

# @router.put("/user/update/{userId}")
# def update_user_detail(userId:str, user_update: schemas.UserUpdateDetail, db:Session=Depends(get_db), get_current_user: User = Depends(get_current_user)):
#     db_user=db.query(models.User).filter(models.User.userId==userId).first()

#     if get_current_user.user_role != UserRole.admin:
#         raise HTTPException(status_code=403, detail = 'not authorized')

#     if not db_user:
#         raise HTTPException(status_code=404,detail="User not found")
    
#     update_data= user_update.dict(exclude_unset=True)
#     PLACEHOLDER_VALUES={"string","user@example.com","9876543210"}
#     cleaned_data = {
#         k:v
#         for k, v in update_data.items()
#         if v is not None and str(v).strip() !="" and str(v).strip() not in PLACEHOLDER_VALUES          
#         }

#     if not cleaned_data:
#         raise HTTPException(status_code=400, detail="no valid fields provided for update")
    
#     UNIQUE_FIELDS = ["mobile", "email"]

#     for field in UNIQUE_FIELDS:
#         if field in cleaned_data:
#             existing_user = db.query(models.User).filter(
#                 getattr(models.User, field) == cleaned_data[field],
#                 models.User.userId != userId  
#             ).first()
#             if existing_user:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"{field} already in use"
#                 )

    
#     for key, value in cleaned_data.items():
#         setattr(db_user, key, value)

#         db_user.updatedAt = datetime.now()
#         db.commit()

#         return {"message": "User updated successfully"}

#     db.commit()
#     return{'messgae':"data of user has been updated"}



# @router.delete("/user/{userId}")
# def delete_user(userId:str,db:Session=Depends(get_db),get_current_user:User = Depends(get_current_user)):
#     user = db.query(models.User).filter(models.User.userId == userId).first()

#     if get_current_user.user_role != UserRole.admin:
#         raise HTTPException(status_code=403, detail = 'not authorized')

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     db.query(models.Logged).filter(models.Logged.userId==userId).delete()
#     db.query(models.Task).filter(
#         or_(
#         (models.Task.assignedby==userId),
#         (models.Task.assignedto==userId)
#         )
#     ).delete()

#     db.delete(user)
#     db.commit()
#     return{"detail":"User deleted sucessfully"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from task_management_system import schemas
from task_management_system.models import UserRole,User
from task_management_system.database import get_db
from task_management_system.utils.dependencies import get_current_user
from task_management_system.crud import crud_user

router = APIRouter()

@router.get("/users", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)

@router.post("/create-user")
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        created_user = crud_user.create_user(user, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "User created", "userId": created_user.userId}

@router.put("/user/update/{userId}")
def update_user_detail(
    userId: str,
    user_update: schemas.UserUpdateDetail,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    if current_user.user_role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = user_update.dict(exclude_unset=True)
    PLACEHOLDER_VALUES = {"string", "user@example.com", "9876543210"}
    cleaned_data = {
        k: v for k, v in update_data.items()
        if v is not None and str(v).strip() != "" and str(v).strip() not in PLACEHOLDER_VALUES
    }

    if not cleaned_data:
        raise HTTPException(status_code=400, detail="No valid fields provided")

    try:
        crud_user.update_user(userId, cleaned_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "User updated successfully"}

@router.delete("/user/{userId}")
def delete_user(
    userId: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    if current_user.user_role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        crud_user.delete_user(userId, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"detail": "User deleted successfully"}
