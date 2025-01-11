import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlmodel import Session

from config.database import engine
from crud.user_crud import get_user_by_email
from models.token import TokenData
from models.user import User, UserPublic

load_dotenv()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS"))
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, os.getenv("SECRETKEY"), algorithm=os.getenv("ALGORITHM")
    )


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now() + timedelta(
        days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, os.getenv("SECRETKEY"), algorithm=os.getenv("ALGORITHM")
    )


def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, os.getenv("SECRETKEY"), algorithms=os.getenv("ALGORITHM")
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = TokenData(username=email)
    except jwt.InvalidTokenError:
        raise credentials_exception
    with Session(engine) as session:
        user: User | None = get_user_by_email(session, token_data.username)
        if user is None:
            raise credentials_exception
    return UserPublic(**user.model_dump())
