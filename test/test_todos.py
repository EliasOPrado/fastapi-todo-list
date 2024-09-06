from main import app
from db.session import get_db
from starlette import status

from .utils import *

app.dependency_overrides[get_db] = override_get_db


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