from sqlalchemy.orm import Session
from app.dtos.user_dtos import UserCreateDTO, UserCreatedDTO
from app.infrastructure.repositories.user_repo import SqlAlchemyUserRepository

class CreateUserUseCase:
    def __init__(self, session: Session):
        self.repo = SqlAlchemyUserRepository(session)

    def execute(self, dto: UserCreateDTO) -> UserCreatedDTO:
        data = self.repo.create(username=dto.username, email=dto.email, posts_count=dto.posts or 0)
        return UserCreatedDTO(id=data["id"], username=data["username"])
