from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class TokenCreate(SQLModel):
    refresh_token: str


class TokenData(SQLModel):
    username: str


class TokenBlacklist(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str
