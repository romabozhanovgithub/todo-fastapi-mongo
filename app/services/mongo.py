from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from app.core import settings
from app.db.client import get_client


class MongoService:
    def __init__(
        self,
        client: AsyncIOMotorClient = None,
        db_name: str = settings.DB_NAME,
    ) -> None:
        if client is None:
            client = get_client()
        self.client = client
        self.db_name = db_name

    def get_db(self) -> AsyncIOMotorDatabase:
        return self.client[self.db_name]

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        db = self.get_db()
        return db[collection_name]
