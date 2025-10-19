from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


class Chatstore(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    Sendername: str
    Recievername: str
    message: str
    timestamp: Optional[str] = (
        None  # Assuming timestamp is a string, adjust as necessary
    )
