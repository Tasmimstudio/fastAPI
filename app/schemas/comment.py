from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str
    parent_comment_id: Optional[str] = None

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    element_id_property: str
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int = 0
    author_username: Optional[str] = None
    parent_comment_id: Optional[str] = None
    replies_count: Optional[int] = 0