from motor.motor_asyncio import AsyncIOMotorClient

from app.core import settings

client = AsyncIOMotorClient(settings.DB_URL)
