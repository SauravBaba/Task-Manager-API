


from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(max_length=30)
    email: EmailStr
    

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, max_length=30)
    email: Optional[EmailStr] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)

class UserOut(UserBase):
    id: int
    is_active:bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
