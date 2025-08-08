from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from app.infrastructure.db.models import UserORM

class SqlAlchemyUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, username: str, email: str, posts_count: int) -> dict:
        user = UserORM(username=username, email=email, posts_count=posts_count or 0)
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            constraint = getattr(getattr(e.orig, "diag", None), "constraint_name", "") or ""
            c = constraint.lower()
            if "username" in c:
                raise ValueError("duplicate_username")
            if "email" in c:
                raise ValueError("duplicate_email")
            raise ValueError("duplicate_user")
        self.session.refresh(user)
        return {"id": user.id, "username": user.username, "posts_count": user.posts_count}

    def list_with_posts(self, offset: int, limit: int) -> tuple[int, list[dict]]:
        total = self.session.scalar(select(func.count()).select_from(UserORM)) or 0

        users = (
            self.session.execute(
                select(UserORM)
                .options(selectinload(UserORM.posts))
                .order_by(UserORM.id)
                .offset(offset)
                .limit(limit)
            )
            .scalars()
            .all()
        )

        result = []
        for u in users:
            posts = [
                {
                    "id": p.id,
                    "user_id": p.user_id,
                    "content": p.content,
                    "likes": p.likes,
                    "created_at": p.created_at,
                }
                for p in u.posts
            ]
            result.append(
                {"id": u.id, "username": u.username, "posts_count": u.posts_count, "posts": posts}
            )
        return total, result
