from datetime import datetime, timedelta
from typing import Any, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException

from app.core import settings
from app.services import UserService
from app.schemas import UserResponseSchema, UserDBSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def verify_password(self, plain_password, hashed_password) -> bool:
        """
        Verify a plain password against a hashed password.
        """

        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        """
        Get password hash.
        """

        return pwd_context.hash(password)

    def create_access_token(self, subject: Union[str, Any]) -> str:
        """
        Create access token.
        """

        encoded_jwt = self._create_token(
            subject, settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return encoded_jwt

    def create_refresh_token(self, subject: Union[str, Any]) -> str:
        """
        Create refresh token.
        """

        encoded_jwt = self._create_token(
            subject, settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        return encoded_jwt

    def _create_token(self, subject: Union[str, Any], expires: int) -> str:
        """
        Create token.
        """

        expires_delta = datetime.utcnow() + timedelta(minutes=expires)
        to_encode = {"exp": expires_delta, "sub": subject}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str) -> str:
        """
        Decode token.
        """

        decoded_token = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token
    
    async def get_current_user(self, token: str) -> UserDBSchema:
        """
        Get current user.
        """

        try:
            payload = self.decode_token(token)
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=401, detail="Could not validate credentials"
                )
        except JWTError:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        user = await self.user_service.get_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_current_active_user(self, token: str) -> UserDBSchema:
        """
        Get current active user.
        """

        current_user = await self.get_current_user(token)
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    async def authenticate_user(
        self, email: str, password: str
    ) -> UserResponseSchema | bool:
        """
        Authenticate user.
        """

        try:
            user = await self.user_service.get_user_by_email(email)
        except self.user_service.not_found_exception:
            return False
        if not self.verify_password(password, user.password):
            return False
        return UserResponseSchema(**user.dict())

    async def sign_up_user(
        self, full_name: str, email: str, password: str
    ) -> UserResponseSchema:
        """
        Sign up user.
        """

        try:
            await self.user_service.find_document_by_field("email", email)
            raise HTTPException(
                status_code=400, detail="Email already registered"
            )
        except self.user_service.not_found_exception:
            user = await self.user_service.create_user(
                {
                    "full_name": full_name,
                    "email": email,
                    "password": self.get_password_hash(password),
                }
            )
            return user
