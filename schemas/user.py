from pydantic import BaseModel


class BaseUser(BaseModel):
    username:str
    
class UserCreate(BaseUser):
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
    
