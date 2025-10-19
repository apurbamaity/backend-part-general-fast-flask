from sqlmodel import SQLModel, create_engine, Session, Field
from models.hero import Hero  # Importing the Hero model to register with metadata
from models.hero import (
    Chatstore,
)  # Importing the Chatstore model to register with metadata


sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully.")
