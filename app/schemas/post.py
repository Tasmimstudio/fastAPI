from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PostCreate(BaseModel):
    content: str
    image_url: Optional[str] = None

class PostUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None

class PostResponse(BaseModel):
    element_id_property: str
    content: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    author_username: Optional[str] = None