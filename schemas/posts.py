from pydantic import BaseModel,Field

class PostSchema(BaseModel):
    title: str = Field(...,min_length=3,max_length=40)
    description: str = Field(...,min_length=3,max_length=500)

class PostResponse(BaseModel):
    id: int
    title: str
    description: str
    user: str
    user_display_name: str | None = None
    user_avatar: str | None = None

    class Config:
        from_attributes = True
    
    
    