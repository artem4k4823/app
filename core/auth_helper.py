from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .config import settings
from app.schemas.token import Token
from app.schemas.user import UserAuth
from fastapi import HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12,)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

def decode_jwt(token:Token) -> dict:
    try:
        return jwt.decode(token, str(settings.SECRET_KEY), str)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

