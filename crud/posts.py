from app.core.models import User
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.core.database import db
from fastapi import Depends
from typing import Annotated, Tuple
from app.crud.auth import get_current_user
from app.schemas.posts import PostSchema
from app.core.models import Post



async def get_all_posts(session: AsyncSession):
    stmt = select(Post).order_by(Post.id)
    result = await session.scalars(stmt)
    posts = result.all()
    return posts
    
async def create_some_post(session:AsyncSession, post: PostSchema, username:str):
    post_data = post.model_dump()
    post_data['user'] = username
    db_post = Post(**post_data)
    session.add(db_post)
    await session.commit()
    return db_post

async def get_some_post_by_id(session:AsyncSession, post_id:int):
    stmt = select(Post).where(Post.id == post_id)
    result = await session.execute(stmt)
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post



async def delete_some_post(session:AsyncSession, post_id: int):
    stmt = delete(Post).where(Post.id == post_id)
    await session.execute(stmt)

    
# def add_favorite_post(user: UserAddFavorite, post_id: int):
#     if post_id not in user.favorite_posts_ids:
#         user.favorite_posts_ids.append(post_id)
        
# def remove_favorite_post(user: UserAddFavorite, post_id: int):
#     if post_id in user.favorite_posts_ids:
#         user.favorite_posts_ids.remove(post_id)
        