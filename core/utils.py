import os
import shutil
from app.schemas.user import UserSchema
from fastapi import UploadFile

def avatar_saver(avatar: UploadFile, user: UserSchema):
    upload_dir = "app/static/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_extension = avatar.filename.split('.')[-1]
    file_name = f"{user.username}_avatar.{file_extension}"
    file_path = os.path.join(upload_dir, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)
        
    user.avatar = f"/static/avatars/{file_name}"