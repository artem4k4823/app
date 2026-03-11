from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional

class BaseUser(BaseModel):
    username:str
    
class UserSchema(BaseUser):
    isAdmin: bool
    status: int
    

class UserCreate(BaseUser):
    displayName: str
    avatar: Optional[UploadFile] = None
    password:str
    
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
    
