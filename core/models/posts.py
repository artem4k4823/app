from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from email.policy import default
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base
from .users import User
from typing import Optional, List

class Post(Base):
    __tablename__ = 'posts'
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(default = 1)
    user: Mapped[str] = mapped_column(ForeignKey(User.username, ondelete='CASCADE', onupdate='CASCADE'))
    users: Mapped[str] = relationship('User', back_populates='post')
    comment: Mapped[list["Coment"]] = relationship('Coment', back_populates='posts')
    coments: Mapped[Optional[List[int]]] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=[],
        nullable=True
        
    )
    
    