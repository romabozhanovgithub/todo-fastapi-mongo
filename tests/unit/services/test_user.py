import pytest

from app.services.user import UserService
from app.schemas import UserResponseSchema


@pytest.mark.asyncio
async def test_get_users(user_service: UserService, user_data: dict):
    user_in_db = await user_service.create_user(user=user_data)
    user = UserResponseSchema(**user_in_db.dict())
    users = await user_service.get_users()
    assert user in users.users


@pytest.mark.asyncio
async def test_get_user(user_service: UserService, user_data: dict):
    user = await user_service.create_user(user=user_data)
    user_from_db = await user_service.get_user(user_id=str(user.id))
    assert user.email == user_from_db.email


@pytest.mark.asyncio
async def test_get_user_by_email(user_service: UserService, user_data: dict):
    user = await user_service.create_user(user=user_data)
    user_from_db = await user_service.get_user_by_email(email=user.email)
    assert user.email == user_from_db.email


@pytest.mark.asyncio
async def test_create_user(user_service: UserService, user_data: dict):
    user = await user_service.create_user(user=user_data)
    assert user.email == user_data["email"]
    assert user.is_active is True
    assert user.id is not None


@pytest.mark.asyncio
async def test_update_user(user_service: UserService, user_data: dict):
    user = await user_service.create_user(user=user_data)
    user.full_name = "New Name"
    user_from_db = await user_service.update_user(
        user_id=str(user.id), user=user.dict()
    )
    assert user_from_db.full_name == "New Name"


@pytest.mark.asyncio
async def test_delete_user(user_service: UserService, user_data: dict):
    user = await user_service.create_user(user=user_data)
    user_from_db = await user_service.delete_user(user_id=str(user.id))
    with pytest.raises(user_service.not_found_exception):
        await user_service.get_user(user_id=str(user.id))
    assert user_from_db.email == user.email
