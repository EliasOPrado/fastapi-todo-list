import pytest
from sqlalchemy import create_engine, text
from fastapi.testclient import TestClient
from db.session import Base
from main import app
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from db.session import get_db
from db.models import Todos
from starlette import status

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Test title",
        description="Test description",
        completed=True
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM TODOS;"))
        connection.commit()