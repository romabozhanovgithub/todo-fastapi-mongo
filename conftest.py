from motor.motor_asyncio import AsyncIOMotorClient
import pytest
from app.core.exceptions import BaseHTTPException
from app.services.base import BaseService
from app.services.mongo import MongoService


@pytest.fixture
def mongo_service():
    mongo_service = MongoService()
    return mongo_service


@pytest.fixture
def base_service(mongo_service):
    class NotFoundException(BaseHTTPException):
        status_code = 404
        detail = "Not Found"

    base_service = BaseService(mongo_service, "test_collection", NotFoundException)
    return base_service
