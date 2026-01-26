from app.core.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserMe, UserAuth
from app.core.auth_helper import hash_password, verify_password
from fastapi import HTTPException, status
from app.core.auth_helper import decode_jwt
from app.core.database import db
from jose import JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from typing import Annotated

http_bearer = HTTPBearer()

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

async def get_user_by_usernames(session:AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
    
    

def get_current_token_payload(creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = creds.credentials
    payload = decode_jwt(token=token)
    return payload

async def get_current_user(
    session: Annotated[AsyncSession, Depends(db.session_getter)], 
    payload: dict = Depends(get_current_token_payload)
):
    username = payload.get('sub')
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
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

