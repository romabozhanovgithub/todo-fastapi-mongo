from app.core import settings
from app.db import client


class MongoService:
    def __init__(self, client=client, db_name=settings.DB_NAME):
        self.client = client
        self.db_name = db_name

    async def get_db(self):
        return self.client[self.db_name]
    
    async def get_collection(self, collection_name):
        db = await self.get_db()
        return db[collection_name]
