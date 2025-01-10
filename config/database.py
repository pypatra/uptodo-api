import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()


database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
