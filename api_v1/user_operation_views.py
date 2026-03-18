from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.security import HTTPBearer
from app.core.database import db
from app.crud.auth import get_current_user
from app.crud.user import get_all_users, create_user, get_user_by_id, get_user_by_usernames, delete_user
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.core.models import User
from typing import Tuple, List
from fastapi import UploadFile

router = APIRouter(prefix='/user', tags=['User_manage'])
http_bearer = HTTPBearer()

@router.get('/get_all_users', response_model=List[UserResponse])
async def get_users(
    deps: Tuple[User, AsyncSession] = Depends(get_current_user)
):
    user, session = deps
    if not user.isAdmin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    
    users = await get_all_users(session=session)    
    return users

@router.post('/create_user')
async def create_users(
    session: Annotated[AsyncSession, Depends(db.session_getter)], 
    username: str = Form(...),  
    displayName: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile = File(None)
):
    user_create = UserCreate(username=username, displayName=displayName, password=password, avatar=avatar)
    users = await create_user(session=session, user_create=user_create)
    return users

@router.delete('/delete_user')
async def delete_user_by_id(user_id: int,deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    if user.isAdmin and user.status == True and user_id != user.id:
        await delete_user(session=session, user_id=user_id)
        return f'user with id: {user_id} was deleted'
    else:
        return 'your are not admin'

@router.get('/get_user_by_id', response_model=UserResponse, dependencies=[Depends(HTTPBearer())])  
async def get_some_user_by_id(
    user_id: int, 
    deps: Tuple[User, AsyncSession] = Depends(get_current_user)
):
    user, session = deps
    
    found_user = await get_user_by_id(session=session, user_id=user_id)
    return found_user

@router.get('/get_user_by_username', response_model=UserResponse)
async def get_some_user_by_usernames(username:str ,session: Annotated[AsyncSession, Depends(db.session_getter)]):
    users = await get_user_by_usernames(session=session, username=username)
    return users
    
@router.patch('/ban_user')
async def ban_user_by_id(user_id: int, deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    if user.isAdmin and user.status == True and user_id != user.id:
        found_user = await get_user_by_id(session=session, user_id=user_id)
        if found_user:
            found_user.status = False
            await session.commit()
            return f'user with id: {user_id} was banned'
        else:
            return f'user with id: {user_id} not found'
    else:
        return HTTPException(status_code=403, detail="Admin access required ")
    
@router.patch('/unban_user')
async def unban_user_by_id(user_id: int, deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    if user.isAdmin and user.status == True and user_id != user.id:
        found_user = await get_user_by_id(session=session, user_id=user_id)
        if found_user:
            found_user.status = True
            await session.commit()
            return f'user with id: {user_id} was unbanned'
        else:
            return f'user with id: {user_id} not found'
    else:
        return HTTPException(status_code=403, detail="Admin access required ")