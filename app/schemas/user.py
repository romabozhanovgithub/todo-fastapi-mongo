from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

from app.schemas import PyObjectId


class UserConfig:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class UserBaseSchema(BaseModel):
    full_name: str = Field(...)
    email: str = Field(...)


class UserRequestSchema(UserBaseSchema):
    password: str = Field(...)

    class Config(UserConfig):
        schema_extra = {
            "example": {
                "full_name": "User 1",
                "email": "example@gmail.com",
                "password": "password",
            }
        }


class UserDBBaseSchema(UserBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    is_active: bool = Field(True)
    created_at: datetime = Field(...)


class UserDBSchema(UserDBBaseSchema):
    password: str = Field(...)


class UserResponseSchema(UserDBBaseSchema):
    class Config(UserConfig):
        schema_extra = {
            "example": {
                "_id": "60c4b8b7e6a9d9f9f7f7f7f7",
                "full_name": "User 1",
                "email": "example@gmail.com",
                "created_at": "2021-01-01 00:00:00",
            }
        }


class UserListResponseSchema(BaseModel):
    users: list[UserResponseSchema] = Field(...)

    class Config(UserConfig):
        schema_extra = {
            "example": {
                "users": [
                    {
                        "_id": "60c4b8b7e6a9d9f9f7f7f7f7",
                        "full_name": "User 1",
                        "email": "example@gmail.com",
                        "created_at": "2021-01-01 00:00:00",
                    },
                    {
                        "_id": "60c4b8b7e6a9d9f9f7f7f7f8",
                        "full_name": "User 2",
                        "email": "example2@gmail.com",
                        "created_at": "2021-01-01 00:00:00",
                    },
                ]
            }
        }


class UserNotFound(Exception):
    detail: str = "User not found"

    class Config(UserConfig):
        schema_extra = {
            "example": {"detail": "User 60c4b8b7e6a9d9f9f7f7f7f7 not found"}
        }
