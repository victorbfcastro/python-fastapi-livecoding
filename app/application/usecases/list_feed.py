from sqlalchemy.orm import Session
from app.dtos.post_dtos import FeedPageDTO, PostDTO
from app.infrastructure.repositories.post_repo import SqlAlchemyPostRepository

class ListFeedUseCase:
    def __init__(self, session: Session):
        self.repo = SqlAlchemyPostRepository(session)

    def execute(self, page: int, size: int) -> FeedPageDTO:
        offset = (page - 1) * size
        total, items = self.repo.list_feed(offset=offset, limit=size)
        return FeedPageDTO(page=page, size=size, total=total, items=[PostDTO(**i) for i in items])
