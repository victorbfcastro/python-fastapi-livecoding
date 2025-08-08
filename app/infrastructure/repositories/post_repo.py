from sqlalchemy.orm import Session
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from app.infrastructure.db.models import PostORM, UserORM
from sqlalchemy import func

class SqlAlchemyPostRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: int, content: str) -> dict:
        # Ensure user exists and increment posts_count
        user = self.session.get(UserORM, user_id)
        if not user:
            raise ValueError("User not found")
        post = PostORM(user_id=user_id, content=content, likes=0)
        user.posts_count = (user.posts_count or 0) + 1
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return {
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "likes": post.likes,
            "created_at": post.created_at,
        }

    def like(self, post_id: int):
        post = self.session.get(PostORM, post_id)
        if not post:
            return None
        post.likes = (post.likes or 0) + 1
        self.session.commit()
        self.session.refresh(post)
        return {
            "id": post.id,
            "user_id": post.user_id,
            "content": post.content,
            "likes": post.likes,
            "created_at": post.created_at,
        }

    def list_feed(self, offset: int, limit: int):
        from app.infrastructure.db.models import PostORM
        q = self.session.execute(
            select(PostORM).order_by(PostORM.created_at.desc(), PostORM.id.desc()).offset(offset).limit(limit)
        ).scalars().all()

        # Total via count(*)
        total = self.session.scalar(select(func.count()).select_from(PostORM)) or 0

        items = [
            {"id": p.id, "user_id": p.user_id, "content": p.content, "likes": p.likes, "created_at": p.created_at}
            for p in q
        ]
        return total, items
