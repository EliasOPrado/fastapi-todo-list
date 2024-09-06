from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todosapp.db")

# Create the SQLAlchemy engine
if DATABASE_URL.startswith("postgresql"):
    # For PostgreSQL, no additional args are needed
    engine = create_engine(DATABASE_URL)
else:
    # For SQLite, use connect_args to avoid check_same_thread issue
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()