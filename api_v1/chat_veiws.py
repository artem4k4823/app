from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select, and_, or_
import json
from app.schemas.message import MessageCreate, MessageResponse
from app.core.database import db
from app.core.models.users import User, Message
from app.crud.auth import get_current_user
from typing import Tuple, Annotated
from app.crud.user import get_user_by_id
from app.schemas.user import UserResponse


router = APIRouter(prefix='/chat', tags=['Chat'])


active_connections = {}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    
    try:
        while True:
            
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            
            event_type = message_data.get("type", "message")
            
            
            if event_type in ["message", "chat_message"]:
                
                receiver_id = message_data.get("receiver_id")
                if receiver_id in active_connections:
                    await active_connections[receiver_id].send_text(json.dumps({
                        "type": "chat_message",
                        "sender_id": user_id,
                        "content": message_data["content"]
                    }))
            
            elif event_type == "ping":
                
                await websocket.send_text(json.dumps({"type": "pong"}))
            
            else:
                
                await broadcast_to_all(message_data, exclude_user=user_id)
    
    except WebSocketDisconnect:
        
        if user_id in active_connections:
            del active_connections[user_id]
        print(f"User {user_id} disconnected")


async def broadcast_to_all(data: dict, exclude_user: int = None):
 
    disconnected = []
    
    for user_id, connection in active_connections.items():
        
        if user_id == exclude_user:
            continue
        
        try:
            await connection.send_text(json.dumps(data))
            print(f"✅ Sent to user {user_id}: {data.get('type')}")
        except:
            
            disconnected.append(user_id)
            print(f"❌ Failed to send to user {user_id}")
    
    
    for user_id in disconnected:
        if user_id in active_connections:
            del active_connections[user_id]

@router.post('/send-message', response_model=MessageResponse)
async def send_message(message: MessageCreate, deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    receiver = await get_user_by_id(session=session, user_id=message.receiver_id)
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if len(message.content) > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message content is too long")
    db_message =Message(
        sender_id = user.id,
        receiver_id = message.receiver_id,
        content = message.content
        
    )
    session.add(db_message)
    await session.commit()
    await session.refresh(db_message)
    return db_message

@router.get("/history/{user1_id}/{user2_id}/", response_model=List[MessageResponse])
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


@router.get("/unread/{user_id}/")
async def get_some_unread_messages(deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    stmt = select(Message).where(and_(Message.receiver_id == user.id, Message.is_read == 0))
    result = await session.execute(stmt)
    unread_messages = result.scalars().all()
    return unread_messages


@router.get('/all-your-chats', response_model=List[UserResponse])
async def get_all_my_chats(deps: Tuple[User, AsyncSession] = Depends(get_current_user)):
    user, session = deps
    stmt = select(Message).where(or_(Message.sender_id == user.id, Message.receiver_id == user.id)).order_by(Message.created_at.desc())
    result = await session.execute(stmt)
    messages = result.scalars().all()
    
    chat_partner_ids = []
    for message in messages:
        if message.sender_id == user.id:
            chat_partner_id = message.receiver_id
        else:
            chat_partner_id = message.sender_id
        
        if chat_partner_id not in chat_partner_ids:
            chat_partner_ids.append(chat_partner_id)
            
    if chat_partner_ids:
        stmt = select(User).where(User.id.in_(chat_partner_ids))
        result = await session.execute(stmt)
        return result.scalars().all()
    
    return []
