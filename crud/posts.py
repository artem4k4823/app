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