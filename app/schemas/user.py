from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    role:str="patient"

class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class UserResponse(BaseModel):
    username:str
    email:EmailStr
    role:str
    id:int
    created_at:datetime
    
    model_config={"from_attributes":True}
    
class Token(BaseModel):
    access_token:str
    token_type:str="bearer"