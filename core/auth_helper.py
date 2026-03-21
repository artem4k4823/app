from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .config import settings
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select
from app.core.models.token import Token
from jose import JWSError, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12,)


if not settings.SECRET_KEY:
    raise ValueError('No secret key')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(entered_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(entered_password,hashed_password)

def create_jwt(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm=str(settings.ALGORITHM))

def decode_jwt(token:str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,  
            algorithms=[settings.ALGORITHM]  
        )
        
        return payload
        
    except (JWSError, JWTError) as e:
        print(f"JWT decode error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    

async def get_token(session: AsyncSession, user_id: int) -> Token | None:
   
    stmt = select(Token).where(Token.user_id == user_id)
    result = await session.execute(stmt)
    token = result.scalar_one_or_none()
    return token
    
async def create_access_token(
    session: AsyncSession, 
    user_id: int, 
    user_data: Optional[dict] = None
) -> dict:
    
    
    jwt_data = {
        'sub': str(user_id),
        'type': 'access',
        'iat': datetime.utcnow().timestamp(),  
    }
    
    if user_data:
        jwt_data.update(user_data)
    
   
    access_token = create_jwt(jwt_data)
    
    
    expire_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    
    existing_token = await get_token(session=session, user_id=user_id)
    
    if existing_token:
        
        existing_token.acces_token = access_token
        existing_token.expire_at = expire_at
    else:
        
        existing_token = Token(
            acces_token=access_token,
            user_id=user_id,
            expire_at=expire_at
        )
        session.add(existing_token)
    
    
    await session.commit()
    await session.refresh(existing_token)
    
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "expires_at": expire_at.isoformat(),
        
    }
    
    