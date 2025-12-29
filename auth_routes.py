#login route to return jwt token
from fastapi import APIRouter,Depends,HTTPException,status
# from fastapi.security import OAuth2PasswordRequestForm,OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from task_management_system.auth import verify_password, create_access_token
from task_management_system.database import SessionLocal,get_db
from task_management_system.models import User
from task_management_system import models,schemas
from datetime import datetime,timedelta
from task_management_system.models import Logged
from task_management_system.utils.dependencies import get_current_user
from task_management_system.utils.expiredtoken import clear_expired_sessions
from task_management_system.utils.idGenerator import generate_custom_id
from task_management_system.schemas import UserLogin, Token





router= APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):    
    clear_expired_sessions(db)

    user = db.query(User).filter(User.name == data.name).first()
    if not user or not verify_password(data.password,user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    db.query(Logged).filter(Logged.userId == user.userId).delete()

    access_token, expires_at = create_access_token(
    data={
        "sub": user.userId,
        "user_role": user.user_role
    }
)

    log_Id = generate_custom_id( db,Logged,'logId',prefix="L")
    new_log = Logged(
        logId=log_Id,
        userId=user.userId,
        token=access_token,
        createdAt=datetime.now(),
        expiresAt=expires_at
    )
    db.add(new_log)
    db.commit()
    print(f"Log inserted: {new_log.logId}")

    # data = db.query(user).first()
    return{"access_token":access_token,"token_type":"bearer"}


