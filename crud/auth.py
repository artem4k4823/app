from app.core.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.core.auth_helper import decode_jwt
from app.core.database import db
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from typing import Annotated
from app.crud.user import chek_user


http_bearer = HTTPBearer()

def get_current_token_payload(creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = creds.credentials
    payload = decode_jwt(token=token)
    return payload

async def get_current_user(
    session: Annotated[AsyncSession, Depends(db.session_getter)], 
    payload: dict = Depends(get_current_token_payload)
):
    username = payload.get('sub')
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = chek_user(session=session, user=user)
    
    
    return user, session

