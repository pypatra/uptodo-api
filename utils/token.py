import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from sqlmodel import Session

from config.database import engine
from crud.user_crud import get_user_by_email
from models.user import User, UserPublic

load_dotenv()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now() + timedelta(days=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")))
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


def verify_access_token(token: str) -> None | UserPublic:
    try:
        payload = jwt.decode(
            token, os.getenv("SECRETKEY"), algorithms=os.getenv("ALGORITHM")
        )

        if payload.get("exp") < datetime.now().timestamp():
            return

        if payload.get("sub") is None:
            return

        with Session(engine) as session:
            existing_user: User | None = get_user_by_email(session, payload.get("sub"))
            if existing_user is None:
                return

        return UserPublic(**existing_user.model_dump())
    except jwt.ExpiredSignatureError:
        return
    except jwt.InvalidTokenError:
        return


def verify_refresh_token(token: str) -> None | UserPublic:
    try:
        payload = jwt.decode(
            token, os.getenv("SECRETKEY"), algorithms=os.getenv("ALGORITHM")
        )

        if payload.get("exp") < datetime.now().timestamp():
            return

        if payload.get("sub") is None:
            return

        with Session(engine) as session:
            existing_user: User | None = get_user_by_email(session, payload.get("sub"))
            if existing_user is None:
                return

        return UserPublic(**existing_user.model_dump())
    except jwt.ExpiredSignatureError:
        return
    except jwt.InvalidTokenError:
        return
