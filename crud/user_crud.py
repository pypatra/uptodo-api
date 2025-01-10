from sqlmodel import Session, select

from models.user import User, UserCreate
from utils.password import get_password_hash


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = session.exec(statement)
    user = result.first()

    return user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement)
    user = result.first()
    return user


def get_user_by_username(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    result = session.exec(statement)
    user = result.first()
    return user


def create_user(session: Session, user_data: UserCreate) -> User:
    user_data.password = get_password_hash(user_data.password)
    user = User(**user_data.model_dump())
    session.add(user)
    session.commit()
    return user


def update_user_refresh_token(session: Session, user_id: int, new_refresh_token: str):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if user is None:
        return False
    user.refresh_token = new_refresh_token
    session.add(user)
    session.commit()
    return True
