from datetime import datetime
from sqlmodel import Session, select

from models.todo import Todo, TodoCreate, TodoDelete, TodoUpdate


def create_todo(session: Session, todo_data: TodoCreate, user_id: int) -> Todo:
    todo = Todo(**todo_data.model_dump(), user_id=user_id)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def get_todos(session: Session, user_id: int):
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos


def update_todo(session: Session, todo_data: TodoUpdate, user_id: int):
    statement = select(Todo).where(Todo.id == todo_data.id, Todo.user_id == user_id)
    todo: Todo | None = session.exec(statement).first()
    if not todo:
        return False
    todo.title = todo_data.title if todo_data.title else todo.title
    todo.description = (
        todo_data.description if todo_data.description else todo.description
    )
    todo.completed = (
        todo_data.completed if todo_data.completed is not None else todo.completed
    )
    todo.updated_at = datetime.now()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def delete_todo(session: Session, todo_data: TodoDelete, user_id: int):
    statement = select(Todo).where(Todo.id == todo_data.id, Todo.user_id == user_id)
    todo: Todo | None = session.exec(statement).first()
    if not todo:
        return False
    session.delete(todo)
    session.commit()
    return todo
