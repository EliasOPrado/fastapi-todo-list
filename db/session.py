from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# SQLALCHECMY_DATABASE_URL = "postgresql://postgres:kb01210012@localhost/TodoApplicationDatabase"

# engine = create_engine(SQLALCHECMY_DATABASE_URL)

SQLALCHECMY_DATABASE_URL = "sqlite:///./todosapp.db"

engine = create_engine(
    SQLALCHECMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
