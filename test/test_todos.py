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

def test_read_all(test_todo):
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["id"] == 1
    assert response.json()[0]['completed'] == True
    assert response.json()[0]['description'] == 'Test description'
    assert response.json()[0]['title'] == 'Test title'

def test_read_one(test_todo):
    response = client.get("/tasks/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()['completed'] == True
    assert response.json()['description'] == 'Test description'
    assert response.json()['title'] == 'Test title'

def test_read_one_not_exists(test_todo):
    response = client.get("/tasks/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Todo not found'

def test_create_todo(test_todo):
    request_data={
        'title': 'New todo from test',
        'description': 'Test description',
        'completed': False
    }
    response = client.post('/tasks/', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['id'] == 2
    assert response.json()['title'] == 'New todo from test'
    assert response.json()['description'] == 'Test description'
    assert response.json()['completed'] == False

def test_update_todo(test_todo):
    request_data={
        'title': 'UPDATED todo from test',
        'description': 'Test description',
        'completed': True
    }
    response = client.put('/tasks/1', json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == test_todo.title
    assert response.json()['description'] == test_todo.description
    assert response.json()['completed'] == test_todo.completed

def test_update_with_patch_payload(test_todo):
    request_data={
        'title': 'PATCH... todo from test',
    }
    response = client.put('/tasks/1', json=request_data)
    assert response.json()['detail'][0]["msg"] == 'Field required'


def test_patch_todo(test_todo):
    request_data={
        'title': 'PATCHED todo from test',
    }
    response = client.patch('/tasks/1', json=request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'PATCHED todo from test'

def test_delete_todo(test_todo):
    response = client.delete('/tasks/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT