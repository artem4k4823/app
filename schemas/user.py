from pydantic import BaseModel


class BaseUser(BaseModel):
    username:str
    
class UserCreate(BaseUser):
    password:str
    
    
class UserAuth(BaseUser):
    password:str
    isAdmin:str