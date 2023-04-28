import asyncio
from bson import ObjectId
import pytest
from app.core.exceptions import BaseHTTPException
from app.services.base import BaseService
from app.services.mongo import MongoService
from app.services.task import TaskService
from app.services.user import UserService


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

# TASKS

@pytest.fixture(scope="session")
def task_service(mongo_service):
    task_service = TaskService(mongo_service)
    return task_service


@pytest.fixture(scope="session")
def task_data():
    task = {
        "title": "Task 1",
        "description": "Task 1 description",
        "status": False,
    }
    return task


@pytest.fixture(scope="session")
def task_data_with_user():
    task = {
        "title": "Task 1",
        "description": "Task 1 description",
        "status": False,
        "user": ObjectId("60f1d1b7e13b9a1e9f1b1b1b"),
    }
    return task

# USERS

@pytest.fixture(scope="session")
def user_service(mongo_service):
    user_service = UserService(mongo_service)
    return user_service


@pytest.fixture(scope="session")
def user_data():
    user = {
        "full_name": "Test User",
        "email": "test@gmail.com",
        "password": "test",
    }
    return user
