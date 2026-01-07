from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey
from .users import User

class Token(Base):
    __tablename__ = 'tokens'
    acces_token: Mapped[str] = mapped_column(unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),unique=True, index=True)
    expire_at: Mapped[datetime]
    user: Mapped['User'] = relationship('User',back_populates='tokens')