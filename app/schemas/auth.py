from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    email: str = Field(..., example="example@gmail.com")
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
