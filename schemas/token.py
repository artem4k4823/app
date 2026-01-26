from pydantic import BaseModel

class TokenSchema(BaseModel):
    username: str
    acces_token:str
    token_type:str

class TokenAuth(BaseModel):
    username: str
