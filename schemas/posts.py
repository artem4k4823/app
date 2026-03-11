from pydantic import BaseModel

class PostSchema(BaseModel):
    title: str
    description: str

class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    user: str
    user_display_name: str | None = None
    user_avatar: str | None = None

    class Config:
        from_attributes = True
    
    
    