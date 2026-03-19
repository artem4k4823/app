from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base
from pydantic import EmailStr
from sqlalchemy import JSON, String, Text, Integer, BigInteger, ForeignKey
from typing import Optional, List
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    displayName: Mapped[str] = mapped_column(nullable=False, unique=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    # is_verified: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[bool] = mapped_column(default=True)
    isAdmin: Mapped[bool] = mapped_column(default=False)
    Token: Mapped[str] = relationship('Token',back_populates='user', foreign_keys='Token.user_id')
    post: Mapped[str] = relationship('Post',back_populates='users')
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    coment: Mapped[list["Coment"]] = relationship('Coment', back_populates='users')


    
    favorite_posts_ids: Mapped[Optional[List[int]]] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=True
    )
    chats: Mapped[Optional[List[int]]] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=True
    )
    messages_sent: Mapped[List["Message"]] = relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender"
    )
    
    messages_received: Mapped[List["Message"]] = relationship(
        "Message",
        foreign_keys="Message.receiver_id",
        back_populates="receiver"
    )


class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    receiver_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    is_read: Mapped[bool] = mapped_column(Integer, default=False)  
    
    sender: Mapped["User"] = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="messages_sent"
    )
    
    receiver: Mapped["User"] = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="messages_received"
    )