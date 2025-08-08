from sqlalchemy.orm import Session
from app.dtos.post_dtos import PostDTO
from app.infrastructure.repositories.post_repo import SqlAlchemyPostRepository

class LikePostUseCase:
    def __init__(self, session: Session):
        self.repo = SqlAlchemyPostRepository(session)

    def execute(self, post_id: int) -> PostDTO | None:
        data = self.repo.like(post_id)
        return PostDTO(**data) if data else None
