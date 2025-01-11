from fastapi import Depends, FastAPI

from routes import auth_route, todo_route

app = FastAPI()


app.include_router(auth_route.router)
app.include_router(todo_route.router)
