from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class StatusEnum(str, PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class PriorityEnum(str, PyEnum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    title= Column(String(100),nullable=False)
    description=Column(String(255))
    status=Column(Enum(StatusEnum, name='status_enum'),default=StatusEnum.pending)
    priority=Column(Enum(PriorityEnum, name='priority_enum'),default=PriorityEnum.medium)
    is_completed=Column(Boolean,default=False)
    due_date=Column(DateTime(timezone=True))
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    user_id=Column(Integer, ForeignKey('users.id'), nullable=False)

    # relationship Task -> User (many-to-one)
    ownerR=relationship("User", back_populates="taskR")


    
