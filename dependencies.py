from typing import Any, Generator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from config.database import engine
from models.user import UserPublic
from utils.token import verify_access_token

oauth2_scheme = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> UserPublic:
    user: None | UserPublic = verify_access_token(token.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
