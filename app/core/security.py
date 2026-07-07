from app.core.config import settings
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#for hashing the password during registration
def hash_password(pasword:str)->str:
    hashed_passowrd= pwd_context.hash(pasword)
    return hashed_passowrd

#for verifying the password during login
def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)



#for creating access token during login
def create_access_token(data:dict)->str:
    print("data",data)
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print("encoded_jwt",encoded_jwt)
    return encoded_jwt

#for decoding access token during login
def decode_access_token(token:str)-> dict | None :
    try:
        payload=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None