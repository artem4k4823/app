from app.core.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.core.auth_helper import hash_password
from fastapi import HTTPException, status

async def get_all_users(session:AsyncSession):
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_user(session: AsyncSession, user_create:UserCreate):
    user = User(**user_create.model_dump())
    password = hash_password(user_create.password)
    user.password = password
    session.add(user)
    await session.commit()
    return user
    
async def get_user_by_id(session:AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

async def get_user_by_usernames(session:AsyncSession, username: UserCreate):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user