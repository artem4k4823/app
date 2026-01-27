from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.core.models import User
from app.crud.auth import get_current_user
from app.crud.posts import get_all_posts, create_some_post
from app.schemas.posts import PostSchema
from typing import Tuple

router = APIRouter(prefix='/post', tags= ['posts'])


@router.get('/get_all_posts')
async def get_all_of_created_posts(deps:Tuple[User,AsyncSession] = Depends(get_current_user)):
    user, session = deps
    if user.status == True:
        posts = await get_all_posts(session=session)
        return posts
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are innactive')

@router.post('/create_post')
async def create_post(post:PostSchema,deps:Tuple[User,AsyncSession] = Depends(get_current_user)):
    user, session = deps
    username = user.username
    post = await create_some_post(session=session, post=post, username=username)
    return post
    
    
    