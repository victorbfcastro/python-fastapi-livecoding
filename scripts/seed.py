import argparse
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import insert
from app.infrastructure.db.session import SessionLocal, engine
from app.infrastructure.db.models import UserORM, PostORM
from tqdm import tqdm

fake = Faker()

def seed(users: int, posts_per_user: int, batch: int):
    session: Session = SessionLocal()
    try:
        # Users in batch
        user_values = [{"username": f"user_{i}", "email": f"user_{i}@test.com", "posts_count": posts_per_user} for i in range(1, users+1)]
        for i in tqdm(range(0, len(user_values), batch), desc="Users"):
            chunk = user_values[i:i+batch]
            session.execute(insert(UserORM), chunk)
            session.commit()

        # Posts in batches
        # 1_000 * 1_000 = 1_000_000 posts → generate in chunks to avoid memory blow
        for uid_start in tqdm(range(1, users+1), desc="Posts per user"):
            uid = uid_start
            post_values = [{"user_id": uid, "content": fake.sentence(nb_words=12), "likes": 0} for _ in range(posts_per_user)]
            for i in range(0, len(post_values), batch):
                chunk = post_values[i:i+batch]
                session.execute(insert(PostORM), chunk)
                session.commit()
        print("Seeding completed.")
    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=1000)
    parser.add_argument("--posts-per-user", type=int, default=1000)
    parser.add_argument("--batch", type=int, default=5000)
    args = parser.parse_args()
    seed(args.users, args.posts_per_user, args.batch)

if __name__ == "__main__":
    main()
