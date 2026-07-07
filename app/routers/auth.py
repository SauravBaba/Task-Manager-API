from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.schemas.auth import TokenOut, LoginRequest
from app.schemas.user import UserOut, UserCreate
from app.database import get_db
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token
router = APIRouter(
    prefix="/auth", 
    tags=["auth"]
)


@router.post("/register",response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
   
   #query email already exists
   existing_user =db.query(models.User).filter(models.User.email==user.email).first()
   if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
   
   user_data = user.model_dump()
   password =user_data.pop("password")
   hashed_password = hash_password(password)
   new_user =models.User(**user_data, hashed_password=hashed_password)
   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user


@router.post("/login",response_model=TokenOut)
def login_user(payload:LoginRequest,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    
    
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    

    access_token = create_access_token({ "user_id": user.id})

    print(access_token)
    return TokenOut(access_token=access_token, token_type="bearer")