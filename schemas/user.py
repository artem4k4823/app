from pydantic import BaseModel,Field
from fastapi import UploadFile
from typing import Optional

class BaseUser(BaseModel):
    username:str = Field(...,min_length=3,max_length=20)
    
class UserSchema(BaseUser):
    isAdmin: bool
    status: int
    

class UserCreate(BaseUser):
    displayName: str = Field(...,min_length=3,max_length=20)
    avatar: Optional[UploadFile] = None
    password:str = Field(...,min_length=3,max_length=40)
    
class UserDelete(BaseUser):
    password:str
    
class UserAuth(BaseUser):
    password:str
    isAdmin:str
    
class UserMe(BaseUser):
    password:str
    token:str
    
class UserResponse(BaseModel):
    id: int
    username: str
    displayName: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True
    
