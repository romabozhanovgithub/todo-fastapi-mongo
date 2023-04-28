from fastapi import HTTPException
import pytest
from unittest.mock import patch
from app.schemas.user import UserResponseSchema

from app.services.auth import AuthService
from app.core.exceptions import UserAlreadyExists, UserInvalidCredentials
from app.services.user import UserService
from app.schemas import UserDBSchema


def test_verify_password(auth_service: AuthService):
    password = "password"
    hashed_password = auth_service.get_password_hash(password)
    assert auth_service.verify_password(password, hashed_password) is None
    with pytest.raises(UserInvalidCredentials):
        auth_service.verify_password("wrong_password", hashed_password)


def test_get_password_hash(auth_service: AuthService):
    password = "password"
    hashed_password = auth_service.get_password_hash(password)
    assert hashed_password != password
    assert auth_service.verify_password(password, hashed_password) is None


@patch("app.services.auth.AuthService._create_token")
def test_create_access_token(auth_service: AuthService):
    token = auth_service.create_access_token("test")
    assert token is not None
    assert auth_service._create_token.called_once_with("test", 1)


@patch("app.services.auth.AuthService._create_token")
def test_create_refresh_token(auth_service: AuthService):
    token = auth_service.create_refresh_token("test")
    assert token is not None
    assert auth_service._create_token.called_once_with("test", 1)


def test_create_token(auth_service: AuthService):
    token = auth_service._create_token("test", 1)
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token(auth_service: AuthService):
    token = auth_service._create_token("test", 1)
    decoded_token = auth_service.decode_token(token)
    assert decoded_token is not None
    assert isinstance(decoded_token, dict)
    assert decoded_token["sub"] == "test"
    assert decoded_token["exp"] is not None
    assert isinstance(decoded_token["exp"], int)


@pytest.mark.asyncio
async def test_get_current_user(
    auth_service: AuthService, user_in_db: UserDBSchema
):
    token = auth_service._create_token(user_in_db.email, 1)
    current_user = await auth_service.get_current_user(token)
    assert current_user is not None
    assert isinstance(current_user, UserDBSchema)
    assert current_user.email == user_in_db.email
    assert current_user.id == user_in_db.id


@pytest.mark.asyncio
async def test_get_current_user_invalid_token_data(auth_service: AuthService):
    token = auth_service._create_token(None, 1)
    with pytest.raises(UserInvalidCredentials):
        await auth_service.get_current_user(token)


@pytest.mark.asyncio
async def test_get_current_user_not_existing_user(auth_service: AuthService):
    token = auth_service._create_token("not_existing_user", 1)
    with pytest.raises(auth_service.user_service.not_found_exception):
        await auth_service.get_current_user(token)


@pytest.mark.asyncio
async def test_get_current_active_user(
    auth_service: AuthService, user_in_db: UserDBSchema
):
    token = auth_service._create_token(user_in_db.email, 1)
    current_user = await auth_service.get_current_active_user(token)
    assert current_user is not None
    assert isinstance(current_user, UserDBSchema)
    assert current_user.email == user_in_db.email
    assert current_user.id == user_in_db.id
    assert current_user.is_active is True


@pytest.mark.asyncio
async def test_get_current_active_user_inactive_user(
    auth_service: AuthService, user_in_db_inactive: UserDBSchema
):
    token = auth_service._create_token(user_in_db_inactive.email, 1)
    with pytest.raises(HTTPException):
        await auth_service.get_current_active_user(token)


@pytest.mark.asyncio
async def test_authenticate_user(
    auth_service: AuthService, user_in_db: UserDBSchema, user_data: dict
):
    user = await auth_service.authenticate_user(
        user_in_db.email, user_data["password"]
    )
    assert user is not None
    assert user.email == user_in_db.email
    assert user.id == user_in_db.id


@pytest.mark.asyncio
async def test_authenticate_user_invalid_credentials(
    auth_service: AuthService, user_in_db: UserDBSchema
):
    with pytest.raises(UserInvalidCredentials):
        await auth_service.authenticate_user(
            user_in_db.email, "invalid_password"
        )


@pytest.mark.asyncio
async def test_authenticate_user_not_existing_user(
    auth_service: AuthService
):
    with pytest.raises(UserInvalidCredentials):
        await auth_service.authenticate_user("not_existing_user", "password")


@pytest.mark.asyncio
async def test_sign_up_user(auth_service: AuthService):
    user = await auth_service.sign_up_user(
        full_name="Test User",
        email="test_email@gmail.com",
        password="password",
    )
    assert user is not None
    assert isinstance(user, UserResponseSchema)
    assert user.email == "test_email@gmail.com"


@pytest.mark.asyncio
async def test_sign_up_user_existing_user(auth_service: AuthService, user_in_db: UserDBSchema):
    with pytest.raises(UserAlreadyExists):
        await auth_service.sign_up_user(
            full_name=user_in_db.full_name,
            email=user_in_db.email,
            password="password",
        )

