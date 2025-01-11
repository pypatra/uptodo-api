from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from crud.user_crud import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    update_user_refresh_token,
)
from dependencies import get_session
from models.token import Token, TokenBlacklist, TokenCreate
from models.user import User, UserCreate, UserLogin, UserPublic
from utils.password import verify_password
from utils.token import create_access_token, create_refresh_token, verify_token

router = APIRouter(
    tags=["Authentications"],
)


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": "Email or username already registered",
            "content": {"application/json": {"example": {"detail": "string"}}},
        }
    },
)
async def user_register(payload: UserCreate, session: Session = Depends(get_session)):
    existing_email: User | None = get_user_by_email(session, payload.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username: User | None = get_user_by_username(session, payload.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    user: User = create_user(session, payload)

    return user


@router.post(
    "/login",
    response_model=Token,
    responses={
        401: {
            "description": "Invalid credentials",
            "content": {"application/json": {"example": {"detail": "string"}}},
        },
    },
)
async def user_login(data: UserLogin, session: Session = Depends(get_session)) -> Token:
    # Check if user exists and password is correct
    existing_user: User | None = get_user_by_email(session, data.email)
    if not existing_user or not verify_password(data.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    # If user does not have a refresh token, create one
    if not existing_user.refresh_token:
        access_token: str = create_access_token({"sub": existing_user.email})
        refresh_token: str = create_refresh_token({"sub": existing_user.email})
        success = update_user_refresh_token(session, existing_user.id, refresh_token)
        if not success:
            raise HTTPException(
                status_code=400, detail="Failed to update refresh token"
            )
        access_token: str = create_access_token({"sub": existing_user.email})
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
    # If user has a refresh token, verify it
    if not verify_token(existing_user.refresh_token):
        access_token: str = create_access_token({"sub": existing_user.email})
        refresh_token: str = create_refresh_token({"sub": existing_user.email})
        success = update_user_refresh_token(session, existing_user.id, refresh_token)
        if not success:
            raise HTTPException(
                status_code=400, detail="Failed to update refresh token"
            )
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    access_token: str = create_access_token({"sub": existing_user.email})

    return Token(
        access_token=access_token,
        refresh_token=existing_user.refresh_token,
        token_type="bearer",
    )


@router.post("/create-access-token", response_model=Token)
async def create_token(
    payload: TokenCreate, session: Session = Depends(get_session)
) -> Token:
    # Verify refresh token
    user = verify_token(payload.refresh_token)
    # Check if token is blacklisted
    token_blacklisted = session.exec(
        select(TokenBlacklist).where(TokenBlacklist.token == payload.refresh_token)
    ).first()
    if token_blacklisted:
        raise HTTPException(status_code=400, detail="Token has been blacklisted")

    access_token: str = create_access_token({"sub": user.email})
    refresh_token: str = create_refresh_token({"sub": user.email})
    success = update_user_refresh_token(session, user.id, refresh_token)
    # Blacklist old refresh token
    token_blacklist = TokenBlacklist(token=payload.refresh_token)
    session.add(token_blacklist)
    session.commit()
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update refresh token")

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )
