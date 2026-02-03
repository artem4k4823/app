from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select, and_, or_
import json
from app.schemas.message import MessageCreate
from app.core.database import db
from app.core.models.users import User, Message
from app.crud.auth import get_current_user
from typing import Tuple, Annotated
from app.crud.user import get_user_by_id


router = APIRouter(prefix='/chat', tags=['Chat'])

active_connections ={}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    
    try:
        while True:
            # Ждем сообщение от клиента
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Отправляем сообщение получателю
            receiver_id = message_data.get("receiver_id")
            if receiver_id in active_connections:
                await active_connections[receiver_id].send_text(json.dumps({
                    "sender_id": user_id,
                    "content": message_data["content"]
                }))
    except WebSocketDisconnect:
        del active_connections[user_id]

@router.post('/send-message')
async def send_message(message: MessageCreate, deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    receiver = get_user_by_id(session=session, user_id=message.receiver_id)
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_message =Message(
        sender_id = user.id,
        receiver_id = message.receiver_id,
        content = message.content
        
    )
    session.add(db_message)
    await session.commit()
    return db_message

@router.get("/history/{user1_id}/{user2_id}/")
async def get_chat_history(
    user1_id: int,
    user2_id: int,
    session: Annotated[AsyncSession, Depends(db.session_getter)]
):
    result = await session.execute(
        select(Message)
        .where(
            or_(
                and_(
                    Message.sender_id == user1_id,
                    Message.receiver_id == user2_id
                ),
                and_(
                    Message.sender_id == user2_id,
                    Message.receiver_id == user1_id
                )
            )
        )
        .order_by(Message.created_at)
    )
    
    messages = result.scalars().all()
    return messages


@router.put("/messages/{message_id}/read/")
async def mark_as_read(message_id: int, session: Annotated[AsyncSession, Depends(db.session_getter)]):
    result = await session.execute(
        select(Message).where(Message.id == message_id)
    )
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = 1
    await session.commit()
    
    return {"status": "message marked as read"}