from app.core.models import User
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserDelete, UserSchema
from app.core.auth_helper import hash_password, verify_password
from fastapi import HTTPException, status, UploadFile
from app.core.auth_helper import decode_jwt
from app.core.database import db
from jose import JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from typing import Annotated, Optional
import os
import shutil

http_bearer = HTTPBearer()

async def get_all_users(session:AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_user(session: AsyncSession, user_create:UserCreate):
    
    avatar_path = None
    if user_create.avatar:
        upload_dir = "app/static/avatars"
        os.makedirs(upload_dir, exist_ok=True)
        
        
        file_extension = user_create.avatar.filename.split('.')[-1]
        file_name = f"{user_create.username}_avatar.{file_extension}"
        file_path = os.path.join(upload_dir, file_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(user_create.avatar.file, buffer)
            
        avatar_path = f"/static/avatars/{file_name}"

    user_data = user_create.model_dump(exclude={'avatar'})
    user = User(**user_data)
    password = hash_password(user_create.password)
    user.password = password
    user.avatar = avatar_path
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(session: AsyncSession, user_id:int):
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()

async def get_user_by_id(session:AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

async def get_user_by_usernames(session:AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
        
async def get_authenticate_user_data(session:AsyncSession, token:str ):
    credentionals_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )
    try:
        payload = decode_jwt(token=token)
        username: str = payload.get('sub')
        if username is None:
            raise credentionals_exeption

    except JWTError:
        raise credentionals_exeption
    user = await get_user_by_usernames(session=session,username = username)
    if user is None:
        raise credentionals_exeption
    return user


def chek_user(session: AsyncSession, user: UserSchema):
    if user.status == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")
    return user