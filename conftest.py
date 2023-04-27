import asyncio
import pytest
from app.core.exceptions import BaseHTTPException
from app.services.base import BaseService
from app.services.mongo import MongoService


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def mongo_service():
    mongo_service = MongoService()
    return mongo_service


@pytest.fixture(scope="session")
def base_service(mongo_service):
    class NotFoundException(BaseHTTPException):
        status_code = 404
        detail = "Not Found"

    base_service = BaseService(
        mongo_service, "test_collection", NotFoundException
    )
    return base_service
