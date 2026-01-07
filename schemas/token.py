from pydantic import BaseModel

class TokenSchema(BaseModel):
    acces_token:str
    token_type:str

