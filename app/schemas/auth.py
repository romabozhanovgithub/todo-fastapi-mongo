from typing import Optional
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., example="example@gmail.com")
    password: str = Field(..., example="password")

    class Config:
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "password",
            }
        }


class SignUpSchema(LoginSchema):
    full_name: str = Field(..., example="User 1")

    class Config:
        schema_extra = {
            "example": {
                "full_name": "User 1",
                "email": "example@gmail.com",
                "password": "password",
            }
        }


class TokenSchema(BaseModel):
    token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
    token_type: str = Field(..., example="bearer")

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "token_type": "bearer",
            }
        }


class TokenDataSchema(BaseModel):
    email: str = Field(..., example="example@gmail.com")

    class Config:
        schema_extra = {"example": {"email": "example@gmail.com"}}


class AccessTokenSchema(BaseModel):
    access_token: str = Field(
        ..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    )
    token_type: str = "bearer"

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "token_type": "bearer",
            }
        }


class InvalidCredentialsSchema(BaseModel):
    detail: str = Field(..., example="Invalid credentials")

    class Config:
        schema_extra = {"example": {"detail": "Invalid credentials"}}


class UserAlreadyExistsSchema(BaseModel):
    detail: str = Field(..., example="User already exists")

    class Config:
        schema_extra = {"example": {"detail": "User already exists"}}


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, regex="password"),
        username: str = Form(),
        password: str = Form(default=""),
        scope: str = Form(default=""),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
    ):
        super().__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )
