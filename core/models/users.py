from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base
from pydantic import EmailStr
from sqlalchemy import String

class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(default=True)
    isAdmin: Mapped[bool] = mapped_column(default=False)
    Token: Mapped[str] = relationship('Token',back_populates='user', foreign_keys='Token.user_id')
    post: Mapped[str] = relationship('Post',back_populates='users')