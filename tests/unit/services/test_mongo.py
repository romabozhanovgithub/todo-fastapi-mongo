import pytest

from app.services.mongo import MongoService


@pytest.mark.asyncio
async def test_get_db(mongo_service: MongoService):
    db = mongo_service.get_db()
    assert db.name == "localhost"


@pytest.mark.asyncio
async def test_get_collection(mongo_service: MongoService):
    collection = mongo_service.get_collection("test_collection")
    assert collection.name == "test_collection"
