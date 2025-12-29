# When defining ForeignKey, you use the table name (as a string).
# When defining relationship, you use the class name (as a string if the class isn’t yet defined).
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text,Time
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from .database import Base

class UserStatus(str,PyEnum):
    active="active"
    inactive="inactive"

class UserRole(str, PyEnum):
    user="user"
    admin="admin"

class TaskStatus(PyEnum):
    todo="todo"
    inprogress="inprogress"
    done="done"

class User(Base):
    __tablename__="users"

    userId= Column(String(5),primary_key=True,index=True)
    name= Column(String(50),nullable=False)
    password= Column(String(500),nullable=False,unique=True)
    mobile=Column(String(10),nullable=False,unique=True)
    email= Column(String(30),nullable=False,unique=True)
    user_role=Column(Enum(UserRole),default=UserRole.user)
    status=Column(Enum(UserStatus),default=UserStatus.active)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now) 

    creator1=relationship("Task",back_populates="assignedby_user",foreign_keys = 'Task.assignedby')
    creator2=relationship("Task",back_populates="assignedto_user",foreign_keys = 'Task.assignedto')
    creator3=relationship("Work",back_populates="userId_user")
    creator5=relationship("Logged",back_populates="userId_user2")


class Task(Base):
    __tablename__="tasks"

    taskId=Column(String(10),primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    description=Column(String(500),nullable=False)
    assignedby=Column(String(5),ForeignKey("users.userId"))
    assignedby_user=relationship("User",back_populates="creator1",foreign_keys=[assignedby])
    assignedto=Column(String(5),ForeignKey("users.userId"))
    assignedto_user=relationship("User",back_populates="creator2",foreign_keys=[assignedto])
    dueDate=Column(DateTime, default=datetime.now, nullable=False)

    status= Column(Enum(TaskStatus),default=TaskStatus.todo)
    createdAt=Column(DateTime, default= datetime.now)
    updatedAt=Column(DateTime, default= datetime.now)
    creator4=relationship("Work",back_populates="taskId_task")

class Work(Base):
    __tablename__="works"

    workId=Column(String(20),primary_key=True,index=True)
    userId=Column(String(5),ForeignKey("users.userId"))
    userId_user=relationship("User",back_populates="creator3")
    taskId=Column(String(10),ForeignKey("tasks.taskId"))
    taskId_task=relationship("Task",back_populates="creator4")
    workDate=Column(DateTime,nullable=False)  
    timeSpent=Column(DateTime)
    createdAt=Column(DateTime,nullable=False,default=datetime.now())
        
class Logged(Base):
    __tablename__="logs"
    logId=Column(String(20),primary_key=True,index=True)
    userId=Column(String(5),ForeignKey("users.userId"))
    userId_user2=relationship("User",back_populates="creator5")
    token=Column(Text)
    expiresAt=Column(DateTime)
    createdAt=Column(DateTime,default=datetime.now,nullable=False)
