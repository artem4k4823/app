from email.policy import default
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base
from .users import User

class Post(Base):
    __tablename__ = 'posts'
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(default = 1)
    user: Mapped[str] = mapped_column(ForeignKey(User.username, ondelete='CASCADE', onupdate='CASCADE'))
    users: Mapped[str] = relationship('User', back_populates='post')
    