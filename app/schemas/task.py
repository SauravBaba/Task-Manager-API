

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import PriorityEnum, StatusEnum


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description:Optional[str] = Field(default=None, max_length=255)
    status: StatusEnum = StatusEnum.pending
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    status: StatusEnum = StatusEnum.pending
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None    

class TaskOut(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TaskListOut(BaseModel):
    total:int
    skip:int 
    limit:int
    tasks:list[TaskOut]

    
    model_config = ConfigDict(from_attributes=True)

        
