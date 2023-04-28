from app.core.dependencies import (
    get_mongo_service,
    get_task_service,
    get_user_service,
    get_auth_service,
)
from app.services import MongoService, TaskService, UserService, AuthService


def test_get_mongo_service():
    mongo_service = get_mongo_service()
    assert mongo_service is not None
    assert isinstance(mongo_service, MongoService)


def test_get_task_service(mongo_service):
    task_service = get_task_service(mongo_service)
    assert task_service is not None
    assert isinstance(task_service, TaskService)


def test_get_user_service(mongo_service):
    user_service = get_user_service(mongo_service)
    assert user_service is not None
    assert isinstance(user_service, UserService)


def test_get_auth_service(user_service):
    auth_service = get_auth_service(user_service)
    assert auth_service is not None
    assert isinstance(auth_service, AuthService)
