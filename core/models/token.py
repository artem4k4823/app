from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey
from .users import User

class Token(Base):
    __tablename__ = 'tokens'
    acces_token: Mapped[str] = mapped_column(unique=True, index=True)
    # username: Mapped[str] = mapped_column(ForeignKey('users.username'), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'),unique=True, index=True, nullable=True)
    expire_at: Mapped[datetime]
    user: Mapped['User'] = relationship('User',back_populates='Token')