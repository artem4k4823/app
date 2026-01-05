from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.schemas.auth_shema import AuthUser
from app.crud.user import get_user_by_usernames
from app.core.auth_helper import verify_password, hash_password
router = APIRouter(prefix='/log', tags=['OAuth'])

@router.post('/login')
async def aunthenticate_user(session: Annotated[AsyncSession, Depends(db.session_getter)], user: AuthUser):
    db_user = await get_user_by_usernames(session=session, username=user.username,)
    if not user or not verify_password(user.password, db_user.password):
        return False
    return user