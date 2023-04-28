from fastapi import FastAPI

from app.core import settings
from app.routers import task_router, auth_router
from app.db.utils import connect_to_mongo, close_mongo_connection

app = FastAPI(title=settings.APP_TITLE)

app.include_router(task_router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await connect_to_mongo()
    print("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    await close_mongo_connection()
    print("Disconnected from MongoDB")
