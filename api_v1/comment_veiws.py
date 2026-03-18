from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.auth import get_current_user
from app.core.models import User
from app.schemas.comment import CommentSchema
from typing import Tuple
from app.core.database import settings
from app.core.models.coment import Coment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.crud.posts import get_some_post_by_id

router = APIRouter(prefix = '/{post_id}/comment', tags=['comment'])


@router.post('/create')
async def create_comment(
    post_id: int,
    comment: CommentSchema,
    user: Tuple[User, AsyncSession] = Depends(get_current_user),
    
):
    user, session = user
    post = await get_some_post_by_id(session=session, post_id=post_id)
    comment = comment.model_dump()
    comment['user'] = user.username
    comment['post'] = post_id
    if post.coments is None:
        post.coments = []
    comment_db = Coment(**comment)
    post.coments.append(comment_db.id)
    session.add(comment_db)
    await session.commit()
    return comment_db

@router.get('/get_all_comments')
async def get_all_comments(post_id: int, deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    stmt = select(Coment).where(Coment.post == post_id)
    result = await session.execute(stmt)
    comments = result.scalars().all()
    return comments
    
    
    
    
