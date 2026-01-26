from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.schemas.auth_shema import AuthUser
from app.crud.user import get_user_by_usernames
from app.core.auth_helper import verify_password,create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer 
from app.core.models import User
from app.crud.auth import get_current_user

router = APIRouter(prefix='/log', tags=['OAuth'])

@router.post('/login')
async def aunthenticate_user(session: Annotated[AsyncSession, Depends(db.session_getter)], user: AuthUser):
    db_user = await get_user_by_usernames(session=session, username=user.username,)
    if not user or not verify_password(user.password, db_user.password):
        return False
    return user

@router.post('/token-login')
async def login( session:Annotated[AsyncSession,Depends(db.session_getter)], data: OAuth2PasswordRequestForm = Depends(), ):
    user = await get_user_by_usernames(session=session,username=data.username)
    user_id = user.id
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )
    
    
    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь неактивен"
        )
    access_token = await create_access_token(session=session, user_id=user_id,user_data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
http_bearer = HTTPBearer()


@router.get('/me')
async def get_my_data(
    user: Annotated[User, Depends(get_current_user)],
):
    return {
        'id': user.id,
        'username': user.username,
        'status': user.status,
        'isAdmin': user.isAdmin
    }