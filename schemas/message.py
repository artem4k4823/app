from pydantic import BaseModel,Field
from datetime import datetime


class MessageBase(BaseModel):
    content: str = Field(...,min_length=1,max_length=500)
    receiver_id: int
    
class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True