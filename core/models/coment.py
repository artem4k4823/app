from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .users import User
from .posts import Post

class Coment(Base):
    __tablename__ = 'coments'
    content: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[str] = mapped_column(ForeignKey(User.username, ondelete='CASCADE', onupdate='CASCADE'))
    post: Mapped[int] = mapped_column(ForeignKey(Post.id, ondelete='CASCADE', onupdate='CASCADE'))
    users: Mapped["User"] = relationship('User', back_populates='coment')
    posts: Mapped["Post"] = relationship('Post', back_populates='comment')