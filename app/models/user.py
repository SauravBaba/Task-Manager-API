from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    username= Column(String(20))
    email=Column(String(50),nullable=False,unique=True)
    hashed_password=Column(String(100),nullable=False)
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())

    #relationship User-> (one to many) with tasks
    taskR=relationship("Task", back_populates="ownerR", cascade="all, delete-orphan")
    
