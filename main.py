from typing import Annotated

from fastapi import Depends, FastAPI

from config.database import create_db_and_tables
from routes import auth_route, todo_route

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(auth_route.router)
app.include_router(todo_route.router)
