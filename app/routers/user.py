from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import schemas, models
from typing import List

router= APIRouter(
    prefix="/users", 
    tags=["users"]
)
 
#create new user
@router.post("/", response_model=schemas.UserOut, status_code=201)
async def createUser(payload:schemas.UserCreate,db:Session=Depends(get_db)):
    user_data = payload.model_dump()
    password = user_data.pop("password")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    new_user=models.User(**user_data, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#get new user by id
@router.get("/{user_id}", response_model=schemas.UserOut)
async def getUser(user_id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#get all users
@router.get("/",response_model=List[schemas.UserOut])
async def getallUser(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users


#update user by id
@router.patch("/{user_id}",response_model=schemas.UserOut)
async def updateUser(user_id:int, payload:schemas.UserUpdate, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

#delete user by id
@router.delete("/{user_id}", response_model=dict, status_code=200)
async def deleteUser(user_id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit() 
    return {"message": "User deleted successfully"}