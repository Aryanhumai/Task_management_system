from sqlalchemy.orm import Session
from sqlalchemy import or_, asc
from datetime import datetime
from task_management_system import models, schemas
from task_management_system.auth import hash_password
from task_management_system.utils.idGenerator import generate_custom_id

def get_all_users(db: Session):
    return db.query(models.User).order_by(asc(models.User.name)).all()


def create_user(user: schemas.UserCreate, db: Session):
    existing_mobile = db.query(models.User).filter(models.User.mobile == user.mobile).first()
    if existing_mobile:
        raise ValueError("Mobile number already exists")

    existing_email = db.query(models.User).filter(models.User.email== user.email.lower()).first()
    if existing_email:
        raise ValueError("Email already registered")

    custom_id = generate_custom_id(db, models.User, 'userId', prefix="U")
    hashed_pwd = hash_password(user.password)

    db_user = models.User(
        userId=custom_id,
        name=user.name,
        password=hashed_pwd,
        mobile=user.mobile,
        email=user.email,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )
    db.add(db_user)
    db.commit()
    return db_user


def update_user(userId: str, update_data: dict, db: Session):
    db_user = db.query(models.User).filter(models.User.userId == userId).first()
    if not db_user:
        raise ValueError("User not found")

    for field in ["mobile", "email"]:
        if field in update_data:
            existing_user = db.query(models.User).filter(
                getattr(models.User, field) == update_data[field],
                models.User.userId != userId
            ).first()
            if existing_user:
                raise ValueError(f"{field} already in use")

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db_user.updatedAt = datetime.now()
    db.commit()
    return db_user


def delete_user(userId: str, db: Session):
    user = db.query(models.User).filter(models.User.userId == userId).first()
    if not user:
        raise ValueError("User not found")

    db.query(models.Logged).filter(models.Logged.userId == userId).delete()
    db.query(models.Task).filter(
        or_(
            models.Task.assignedby == userId,
            models.Task.assignedto == userId
        )
    ).delete()
    db.query(models.Work).filter(
        or_(
            models.Task.assignedby == userId,
            models.Task.assignedto == userId
        )
    ).delete()

    db.delete(user)
    db.commit()
    return True
