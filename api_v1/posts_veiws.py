from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.core.models import User
from app.crud.auth import get_current_user
from app.crud.posts import get_all_posts, create_some_post, get_some_post_by_id, delete_some_post
from app.schemas.posts import PostSchema
from typing import Tuple
from app.core.models.posts import Post
from sqlalchemy import select

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
    
@router.delete('/delete-post')
async def delete_post(post_id: int, deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user,session = deps
    post = await get_some_post_by_id(session=session, post_id=post_id)
    if (post.user == user.username or user.isAdmin == True) and user.status == True:
        await delete_some_post(session=session,post_id=post_id)
        return f'post was deleted by {user.username}'
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='you dont have permision for what')
        
    
@router.post('/add-favorite-post')
async def add_favorite_post(post_id: int, deps: Tuple[User,AsyncSession] = Depends(get_current_user)):
    user, session = deps
    if user.favorite_posts_ids is None:
        user.favorite_posts_ids = []
    if post_id not in user.favorite_posts_ids:
        user.favorite_posts_ids.append(post_id)
        await session.commit()
        return 'post was added'
    return {"status": "added", "post_id": post_id}

@router.post('/remove-favorite-post')
async def remove_favorite_post(post_id: int, deps: Tuple[User,AsyncSession] = Depends(get_current_user)):
    user, session = deps
    if user.favorite_posts_ids is None:
        user.favorite_posts_ids = []
    if post_id in user.favorite_posts_ids:
        user.favorite_posts_ids.remove(post_id)
        await session.commit()
        return 'post was removed'
    return 'you dont have this post in favorite'

@router.get('/get-favorite-posts')
async def get_favorite_posts(
    deps: Tuple[User, AsyncSession] = Depends(get_current_user)
):
    
    user, session = deps
    
    if not user.favorite_posts_ids:
        return [] 
    
    result = await session.execute(
        select(Post).where(Post.id.in_(user.favorite_posts_ids))
    )
    posts = result.scalars().all()
    
    return posts