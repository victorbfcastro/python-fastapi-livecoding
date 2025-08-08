from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.dtos.user_dtos import UserCreateDTO, UserCreatedDTO, UserWithPostsDTO, UsersWithPostsPageDTO
from app.dtos.post_dtos import PostCreateDTO, PostDTO, FeedPageDTO
from app.application.usecases.create_user import CreateUserUseCase
from app.application.usecases.create_post import CreatePostUseCase
from app.application.usecases.like_post import LikePostUseCase
from app.application.usecases.list_feed import ListFeedUseCase
from app.application.usecases.list_users_with_posts import ListUsersWithPostsUseCase
from app.infrastructure.db.session import get_session
from sqlalchemy.orm import Session

api_router = APIRouter()

@api_router.post("/users", response_model=UserCreatedDTO, status_code=201)
def create_user(payload: UserCreateDTO, session: Session = Depends(get_session)):
    uc = CreateUserUseCase(session)
    user = uc.execute(payload)
    return user

@api_router.post("/posts", response_model=PostDTO, status_code=201)
def create_post(payload: PostCreateDTO, session: Session = Depends(get_session)):
    uc = CreatePostUseCase(session)
    post = uc.execute(payload)
    return post

@api_router.post("/posts/{post_id}/like", response_model=PostDTO)
def like_post(post_id: int, session: Session = Depends(get_session)):
    uc = LikePostUseCase(session)
    post = uc.execute(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@api_router.get("/feed", response_model=FeedPageDTO)
def feed(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=200), session: Session = Depends(get_session)):
    uc = ListFeedUseCase(session)
    return uc.execute(page=page, size=size)

@api_router.get("/users-with-posts", response_model=UsersWithPostsPageDTO)
def users_with_posts(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), session: Session = Depends(get_session)):
    uc = ListUsersWithPostsUseCase(session)
    return uc.execute(page=page, size=size)
