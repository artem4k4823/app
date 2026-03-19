from fastapi import UploadFile
from sqlalchemy import select
from typing import Optional
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
from typing import Tuple
from app.core.utils import avatar_saver
router = APIRouter(prefix='/log', tags=['OAuth'])



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
    deps: Tuple[User, AsyncSession] = Depends(get_current_user),
):
    user, session = deps
    return {
        'id': user.id,
        'username': user.username,
        'displayName': user.displayName,
        'status': user.status,
        'isAdmin': user.isAdmin,
        'favorite_posts': user.favorite_posts_ids,
        'avatar': user.avatar,
        # 'comments': user.coment
    }
    
@router.patch('/me/settings')
async def change_data(
    username: Optional[str] = None,
    displayName: Optional[str] = None,
    avatar: Optional[UploadFile] = None,
    deps: Tuple[User, AsyncSession] = Depends(get_current_user)
):
    user, session = deps
    if user:
        user.username = username if username else user.username
        user.displayName = displayName if displayName else user.displayName
        
        if avatar:
            avatar = avatar_saver(avatar=avatar, user=user)
            
        await session.commit()
        return 'data was changed'
    
#test