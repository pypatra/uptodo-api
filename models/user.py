from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: EmailStr


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    refresh_token: str| None = Field(default=None)


class UserCreate(UserBase):
    password: str


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class UserPublic(SQLModel):
    id: int
    username: str
    email: EmailStr
