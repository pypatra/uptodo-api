from datetime import datetime

from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    id: int | None = Field(primary_key=True, index=True)
    title: str
    description: str
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TodoCreate(SQLModel):
    title: str
    description: str


class TodoUpdate(SQLModel):
    id: int
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TodoDelete(SQLModel):
    id: int
