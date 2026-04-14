# app/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User
from app.services.auth_service import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
# tokenUrl tells Swagger UI where the login endpoint is
# It does NOT affect actual security — just for the docs UI

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],    # modern Annotated style
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    user_id = verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id_int = int(user_id)
        # We stored user ID as string in "sub" claim (JWT spec says sub must be string)
        # So we convert back to int here to query the DB
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.id == user_id_int))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# The type alias — this is the BEST part of your style
# Instead of writing Annotated[User, Depends(get_current_user)] in EVERY route,
# you write it once here and use CurrentUser everywhere
CurrentUser = Annotated[User, Depends(get_current_user)]

async def get_current_doctor(current_user: CurrentUser) -> User:
    if current_user.role != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors can perform this action"
        )
    return current_user

CurrentDoctor = Annotated[User, Depends(get_current_doctor)]