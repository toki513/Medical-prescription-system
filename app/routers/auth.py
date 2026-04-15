from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db 
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse,UserLogin,Token
from app.services.auth_service import hash_password,verify_password,create_access_token
from app.dependencies import CurrentUser


