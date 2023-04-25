from fastapi import FastAPI
from app.core import settings
from app.routers import task_router

app = FastAPI(title=settings.APP_TITLE)

app.include_router(task_router)
