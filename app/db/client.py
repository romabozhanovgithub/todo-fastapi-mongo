from motor.motor_asyncio import AsyncIOMotorClient

from app.core import settings

client = AsyncIOMotorClient(f"{settings.DB_HOST}:{settings.DB_PORT}")
