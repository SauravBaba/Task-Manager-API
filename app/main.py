from fastapi import FastAPI

from app.routers import auth, task, user
from app.database import engine, Base
# Import models to ensure they are registered with SQLAlchemy's Base before creating tables
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)