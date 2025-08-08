from sqlalchemy.orm import Session
from app.dtos.user_dtos import UsersWithPostsPageDTO, UserWithPostsDTO
from app.dtos.post_dtos import PostDTO
from app.infrastructure.repositories.user_repo import SqlAlchemyUserRepository

class ListUsersWithPostsUseCase:
    def __init__(self, session: Session):
        self.repo = SqlAlchemyUserRepository(session)

    def execute(self, page: int, size: int) -> UsersWithPostsPageDTO:
        offset = (page - 1) * size
        total, users = self.repo.list_with_posts(offset=offset, limit=size)
        mapped = []
        for u in users:
            mapped.append(UserWithPostsDTO(
                id=u["id"],
                username=u["username"],
                posts_count=u["posts_count"],
                posts=[PostDTO(**p) for p in u["posts"]]
            ))
        return UsersWithPostsPageDTO(page=page, size=size, total=total, users=mapped)
