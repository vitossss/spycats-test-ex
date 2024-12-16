from sqlmodel import SQLModel, create_engine, Session
from .config import DATABASE_URL

# models import for creating db and tables.
from src import models


engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
