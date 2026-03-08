from sqladmin.authentication import AuthenticationBackend
from fastapi import Request, HTTPException, status, Depends
from app.core.database import db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import User
from app.crud.auth import get_current_user
from typing import Tuple
from app.core.config import settings

from typing import Annotated

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get('username'), form.get('password')
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session['token'] = 'admin_token'
            return True
        return False
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request):
        token = request.session.get('token')
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if token == 'admin_token':
            return True 