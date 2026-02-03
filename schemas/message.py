from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str
    receiver_id: int
    
class MessageCreate(MessageBase):
    pass