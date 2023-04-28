from app.core.exceptions import UserNotFound
from app.services.base import BaseService
from app.schemas import (
    UserRequestSchema,
    UserResponseSchema,
    UserListResponseSchema,
    UserDBSchema,
)


class UserService(BaseService):
    collection_name = "users"
    not_found_exception = UserNotFound

    async def get_users(self) -> UserListResponseSchema:
        users = await self.find_documents()
        return UserListResponseSchema(users=users)

    async def get_user(self, user_id: str) -> UserResponseSchema:
        user = await self.find_document_by_id(user_id)
        return UserResponseSchema(**user)

    async def get_user_by_email(self, email: str) -> UserDBSchema:
        user = await self.find_document_by_field("email", email)
        return UserDBSchema(**user)

    async def create_user(self, user: dict) -> UserResponseSchema:
        result = await self.create_document(
            {
                **user,
                "is_active": True,
            }
        )
        return UserResponseSchema(**result)

    async def update_user(
        self, user_id: str, user: dict
    ) -> UserResponseSchema:
        result = await self.find_and_update_document_by_id(
            user_id, user
        )
        return UserResponseSchema(**result)

    async def delete_user(self, user_id: str) -> UserResponseSchema:
        user = await self.find_and_delete_document_by_id(user_id)
        return UserResponseSchema(**user)
