from sqladmin import ModelView
from app.core.models import User
from app.core.models import Post
from app.core.models.users import Message


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.isAdmin, User.status, User.favorite_posts_ids]
    column_searchable_list = [User.username]
    # column_filters = ['isAdmin', 'status']
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'User'
    
class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.title]
    column_searchable_list = [Post.title]
    # column_filters = ['isAdmin', 'status']
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Post'
    
class MessageAdmin(ModelView, model = Message):
    column_list = [Message.id, Message.created_at, Message.sender_id, Message.receiver_id, Message.content]
    column_searchable_list = [Message.id]
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    name = 'Message'