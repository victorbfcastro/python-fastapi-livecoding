from app.infrastructure.db.session import Base, engine
from app.infrastructure.db import models  # noqa

def main():
    Base.metadata.create_all(bind=engine)
    print("DB initialized.")

if __name__ == "__main__":
    main()
