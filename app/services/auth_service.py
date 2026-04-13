from datetime import datetime,UTC,timedelta
from typing import Annotated
import jwt
from pwdlib import PasswordHash
from app.config import settings

password_hash= PasswordHash.recommend()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hash.verify(plain_password,hashed_password)

def create_access_token(data:dict, expires_delta:timedelta | None = None) ->str:
    to_encode=data.copy()
    
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp":expire})
    
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM
    )
    
def verify_access_token(token:str)->str | None:
    try:
        payload=jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithm=[settings.ALGORITHM],
            options={"require":["exp","sub"]},
        )
    except jwt.InvalidTokenError:
        return None
    return payload.get("sub")
        
        
