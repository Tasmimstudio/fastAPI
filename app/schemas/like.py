from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LikeResponse(BaseModel):
    element_id_property: str
    like_type: str
    created_at: datetime
    user_username: Optional[str] = None