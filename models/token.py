from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str
    
class TokenCreate(SQLModel):
    refresh_token: str
