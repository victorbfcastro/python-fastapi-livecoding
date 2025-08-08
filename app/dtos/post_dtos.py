from pydantic import BaseModel, Field
from datetime import datetime

class PostCreateDTO(BaseModel):
    user_id: int
    content: str = Field(..., min_length=1, max_length=500)

class PostDTO(BaseModel):
    id: int
    user_id: int
    content: str
    likes: int
    created_at: datetime

class FeedPageDTO(BaseModel):
    page: int
    size: int
    total: int
    items: list[PostDTO]
