from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas.auth import SignUpSchema

from app.services import AuthService
from app.schemas import (
    TokenSchema,
    AccessTokenSchema,
    UserResponseSchema,
)
from app.core.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    summary="Login",
    response_model=AccessTokenSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    login: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> AccessTokenSchema:
    user = await auth_service.authenticate_user(login.username, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = auth_service.create_access_token(user.email)
    return AccessTokenSchema(
        access_token=token,
        token_type="bearer",
    )


@router.post(
    "/signup",
    summary="Sign Up",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    data: SignUpSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponseSchema:
    user = await auth_service.sign_up_user(**data.dict())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    return user
