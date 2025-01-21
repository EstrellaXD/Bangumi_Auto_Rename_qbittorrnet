from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(
        "admin", min_length=4, max_length=20, regex=r"^[a-zA-Z0-9_]+$"
    )
    password: str = Field("adminadmin", min_length=8)


class UserUpdate(SQLModel):
    username: str|None = Field(
        None, min_length=4, max_length=20, regex=r"^[a-zA-Z0-9_]+$"
    )
    password: str|None = Field(None, min_length=8)


class UserLogin(SQLModel):
    username: str
    password: str = Field(..., min_length=8)


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
