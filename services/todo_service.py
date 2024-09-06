from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Todos
from schemas.todo_schema import TodoRequest


def get_todo_or_404(db: Session, todo_id: int) -> Todos:
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_model


def create_todo_object(db: Session, todo_request: TodoRequest) -> Todos:
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


def update_todo_object(db: Session, todo_request: TodoRequest, todo_id: int) -> Todos:
    # Retrieve the existing todo or raise a 404 error
    todo_model = get_todo_or_404(db, todo_id)

    # Update the todo model with new values
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.completed = todo_request.completed

    db.commit()
    db.refresh(todo_model)

    return todo_model


def patch_todo_object(db: Session, todo_request: TodoRequest, todo_id: int) -> Todos:
    todo_model = get_todo_or_404(db, todo_id)
    # Update only the provided fields
    if todo_request.title is not None:
        todo_model.title = todo_request.title
    if todo_request.description is not None:
        todo_model.description = todo_request.description
    if todo_request.completed is not None:
        todo_model.completed = todo_request.completed

    db.commit()
    db.refresh(todo_model)

    return todo_model


def delete_todo_object(db: Session, todo_id: int) -> Todos:
    todo_model = get_todo_or_404(db, todo_id)
    db.query(Todos).filter(Todos.id == todo_model.id).delete()
    db.commit()
    return None
