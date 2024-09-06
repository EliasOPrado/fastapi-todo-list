from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path
from db.session import get_db
from db.models import Todos
from starlette import status
from schemas.todo_schema import TodoRequest, TodoPatchRequest
from services.todo_service import (
    get_todo_or_404,
    create_todo_object,
    update_todo_object,
    delete_todo_object,
    patch_todo_object,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    return get_todo_or_404(db, todo_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    return create_todo_object(db, todo_request)


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    return update_todo_object(db, todo_request, todo_id)


@router.patch("/{todo_id}", status_code=status.HTTP_200_OK)
async def patch_todo(
    db: db_dependency, todo_request: TodoPatchRequest, todo_id: int = Path(gt=0)
):
    return patch_todo_object(db, todo_request, todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    return delete_todo_object(db, todo_id)
