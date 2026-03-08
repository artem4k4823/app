from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    class Config:
        env_file = '.env'
        case_sensitive = False
        
settings = Settings()