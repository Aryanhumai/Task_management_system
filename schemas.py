from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum
from datetime import datetime,date, time
from typing import Optional,Annotated





#--enum----
class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserStatus(str,Enum):
    active="active"
    inactive="inactive"

class TaskStatus(str,Enum):
    todo="todo"
    inprogress="inprogress"
    done="done"


class UserOut(BaseModel):
    userId:str
    name:str
    email:EmailStr
    # user_role:UserRole    
    # status:UserStatus


class UserCreate(BaseModel):
    name:str = Field(..., pattern=r'^[A-Za-z ]+$', description="Name must contain only letters and spaces")
    password:str = Field(..., min_length=4, description="Password must not be empty")
    mobile:str | None = Field(None, pattern=r'^[6-9]\d{9}$', description="Must be a 10-digit number")
    email:EmailStr
    # user_role:UserRole
    # status:UserStatus

    @field_validator("password")
    def password_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Password cannot be empty or whitespace")
        return v

class UserUpdateDetail(BaseModel):
    name: Optional[str] | None = Field(..., pattern=r'^[A-Za-z ]+$', description="Name must contain only letters and spaces")
    password:Optional[str] | None= Field(..., min_length=4, description="Password must not be empty")
    mobile:Optional[str] | None = Field(None, pattern=r'^[6-9]\d{9}$', description="Must be a 10-digit number")
    email:Optional[EmailStr] = None 

    @field_validator("password")
    def password_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Password cannot be empty or whitespace")
        return v

class TaskCreate(BaseModel):
    name:str = Field(..., pattern=r'^[A-Za-z ]+$', description="Name must contain only letters and spaces")
    description:Optional[str]
    # assignedby:str
    assignedto:str
    dueDate:str =Field(description="date should be in YYYY:MM:DD format")
    status:Optional[TaskStatus]=TaskStatus.todo

    @field_validator("dueDate")
    def validate_due_date(cls, value):
        try:  
            datetime.strptime(value, "%Y:%m:%d")
        except ValueError:
            raise ValueError("dueDate must be in format 'YYYY:MM:DD '")
        return value

class TaskOut(BaseModel):
    taskId: str 
    name: str
    description: Optional[str]
    assignedby: str
    assignedto: str
    dueDate: datetime
    status: TaskStatus
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class TaskUpdateDetails(BaseModel):
    name: str = Field(..., pattern=r'^[A-Za-z ]+$', description="Name must contain only letters and spaces")
    description: Optional[str]
    assignedto: Optional[str] 
    dueDate: str
    status: TaskStatus
    @field_validator("dueDate")
    def validate_due_date(cls, value):
        try:  
            datetime.strptime(value, "%Y:%m:%d")
        except ValueError:
            raise ValueError("dueDate must be in format 'YYYY:MM:DD '")
        return value

    @field_validator("name", "description", "status")
    @classmethod
    def non_empty_fields(cls, v):
        if v is not None and not str(v).strip():
            raise ValueError("Field cannot be empty or whitespace")
        return v

class TaskUpdateStatus(BaseModel):
    status:TaskStatus


    

class WorkCreate(BaseModel):
    # workId:str
    userId:str
    taskId:str
    workDate:datetime
    timeSpent:time = Field(..., description='Enter time in hh:mm:ss', example='00:00:00')
    # createdAt:datetime
   
   
    # @field_validator("dueDate")
    # def validate_due_date(cls, value):
    #     try:  
    #         datetime.strptime(value, "%Y:%m:%d")
    #     except ValueError:
    #         raise ValueError("dueDate must be in format 'YYYY:MM:DD '")
    #     return value

class WorkOut(BaseModel):
    userId:Optional[str]
    taskId:str
    workDate:datetime
    timeSpent:time = Field(..., description='Enter time in hh:mm:ss', example='00:00:00')

class UserLogin(BaseModel):
    name: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str
