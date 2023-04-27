from fastapi import Depends
from app.services import MongoService
from app.services import TaskService


def get_mongo_service() -> MongoService:
    return MongoService()


def get_task_service(
    mongo_service: MongoService = Depends(get_mongo_service),
) -> TaskService:
    return TaskService(mongo_service)
