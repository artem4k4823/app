from fastapi import APIRouter, Depends
from app.core.database import db
from app.crud.user import get_all_users, create_user, get_user_by_id, get_user_by_usernames, delete_user
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate

router = APIRouter(prefix='/user', tags=['User_manage'])

@router.get('/get_all_users')
async def get_users(
    session: Annotated[AsyncSession, Depends(db.session_getter)]
):
    users = await get_all_users(session=session)
    return users

@router.post('/create_user')
async def create_users(
    session: Annotated[AsyncSession, Depends(db.session_getter)], 
    user_create: UserCreate,
):
    users = await create_user(session=session,user_create=user_create)
    return users

@router.delete('/delete_user')
async def delete_user_by_id(session: Annotated[AsyncSession, Depends(db.session_getter)], user_id: int):
    await delete_user(session=session, user_id=user_id)
    return f'user with id: {user_id} was deleted'

@router.get('/get_user_by_id')
async def get_some_user_by_id(session: Annotated[AsyncSession, Depends(db.session_getter)],
                        user_id: int):
    users = await get_user_by_id(session=session, user_id=user_id)
    return users

@router.get('/get_user_by_username')
async def get_some_user_by_usernames(session: Annotated[AsyncSession, Depends(db.session_getter)],
                        username:str ):
    users = await get_user_by_usernames(session=session, username=username)
    return users
    
