from fastapi import Depends
from app.services import MongoService, TaskService, UserService, AuthService
from app.schemas import UserDBBaseSchema
from app.core.utils import oauth2_scheme


def get_mongo_service() -> MongoService:
    return MongoService()


def get_task_service(
    mongo_service: MongoService = Depends(get_mongo_service),
) -> TaskService:
    return TaskService(mongo_service)


def get_user_service(
    mongo_service: MongoService = Depends(get_mongo_service),
) -> UserService:
    return UserService(mongo_service)


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)


async def get_request_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserDBBaseSchema:
    user = await auth_service.get_current_active_user(token)
    return user
