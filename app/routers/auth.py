from fastapi import APIRouter, Depends, Request, status
from app.core.exceptions import UserAlreadyExists
from app.schemas.auth import SignUpSchema

from app.services import AuthService
from app.schemas import (
    AccessTokenSchema,
    UserResponseSchema,
    InvalidCredentialsSchema,
    UserAlreadyExistsSchema,
    CustomOAuth2PasswordRequestForm,
)
from app.core.dependencies import get_auth_service
from app.core.utils import oauth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    summary="Login",
    response_model=AccessTokenSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsSchema}
    },
)
async def login(
    login: CustomOAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> AccessTokenSchema:
    # this is a hack to allow google auth to work
    if not login.password:
        await auth_service.get_current_active_user(login.username)
        return AccessTokenSchema(
            access_token=login.username,
        )
    user = await auth_service.authenticate_user(login.username, login.password)
    token = auth_service.create_access_token(user.email)
    return AccessTokenSchema(
        access_token=token,
    )


@router.post(
    "/signup",
    summary="Sign Up",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"model": UserAlreadyExistsSchema}},
)
async def signup(
    data: SignUpSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponseSchema:
    user = await auth_service.sign_up_user(**data.dict())
    if not user:
        raise UserAlreadyExists()
    return UserResponseSchema(**user.dict())


@router.get(
    "/google",
    summary="Google Auth",
    response_model=AccessTokenSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": InvalidCredentialsSchema}
    },
)
async def google_auth(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> AccessTokenSchema:
    user = await auth_service.google_authenticate_user(request)
    token = auth_service.create_access_token(user.email)
    return AccessTokenSchema(
        access_token=token,
    )


@router.get(
    "/google/login",
    summary="Google Login",
)
async def google_login(
    request: Request,
) -> None:
    redirect_uri = request.url_for("google_auth")
    return await oauth.google.authorize_redirect(request, str(redirect_uri))
