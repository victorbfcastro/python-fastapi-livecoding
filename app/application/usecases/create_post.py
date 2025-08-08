from sqlalchemy.orm import Session
from app.dtos.post_dtos import PostCreateDTO, PostDTO
from app.infrastructure.repositories.post_repo import SqlAlchemyPostRepository

class CreatePostUseCase:
    def __init__(self, session: Session):
        self.repo = SqlAlchemyPostRepository(session)

    def execute(self, dto: PostCreateDTO) -> PostDTO:
        data = self.repo.create(user_id=dto.user_id, content=dto.content)
        return PostDTO(**data)
