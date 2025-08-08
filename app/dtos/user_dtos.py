from pydantic import BaseModel, EmailStr, Field

class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    posts: int | None = 0

class UserCreatedDTO(BaseModel):
    id: int
    username: str

class UserWithPostsDTO(BaseModel):
    id: int
    username: str
    posts_count: int
    posts: list["PostDTO"] = []  # forward ref

from app.dtos.post_dtos import PostDTO  # noqa

class UsersWithPostsPageDTO(BaseModel):
    page: int
    size: int
    total: int
    users: list[UserWithPostsDTO]
