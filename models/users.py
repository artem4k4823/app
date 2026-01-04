from sqlalchemy.orm import mapped_column, Mapped
from ..core.base import Base
from pydantic import EmailStr
from sqlalchemy import String

class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    
    password: Mapped[str] = mapped_column(nullable=False)
