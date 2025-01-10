from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from crud.todo_crud import create_todo, delete_todo, get_todos, update_todo
from dependencies import get_current_user, get_session
from models.todo import Todo, TodoCreate, TodoDelete, TodoUpdate
from models.user import UserPublic

router = APIRouter(
    tags=["Todos"],
    prefix="/todo",
    responses={404: {"description": " Todo Not found"}},
)


@router.get("/", response_model=list[Todo])
async def get_todos_user(
    user: UserPublic = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    todos = get_todos(session, user.id)
    return todos


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo_user(
    payload: TodoCreate,
    user: UserPublic = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    todo: Todo = create_todo(session, payload, user.id)
    return todo


@router.patch("/", response_model=Todo, status_code=status.HTTP_200_OK)
async def update_todo_user(
    payload: TodoUpdate,
    user: UserPublic = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Todo:
    todo = update_todo(session, payload, user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.delete("/", response_model=Todo, status_code=status.HTTP_200_OK)
async def delete_todo_user(
    payload: TodoDelete,
    user: UserPublic = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Todo:
    todo = delete_todo(session, payload, user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo
