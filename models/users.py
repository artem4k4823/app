from sqlalchemy.orm import mapped_column, Mapped
from ..core.base import Base
from pydantic import EmailStr
from sqlalchemy import String

class User(Base):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[EmailStr] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
