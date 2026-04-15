from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db 
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse,UserLogin,Token
from app.services.auth_service import hash_password,verify_password,create_access_token
from app.dependencies import CurrentUser


router = APIRouter(prefix="/api/auth", tags=["Authentication"])

DB = Annotated[AsyncSession,Depends(get_db)]

@router.post("/signup",response_model=UserResponse,status_code=201)
async def signup(user_data:UserCreate, db:DB):
    result=await db.execute(select(User).where(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400,detail="Email already registered")
    
    new_user=User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    return new_user


@router.post("/login",response_model=Token)
async def login(user_data:UserLogin,db:DB):
    result=await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()
    
    