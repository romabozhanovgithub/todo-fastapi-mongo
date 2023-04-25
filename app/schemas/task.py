from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

from app.schemas import PyObjectId


class TaskConfig:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class TaskBaseSchema(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    status: bool = Field(...)

class TaskRequestSchema(TaskBaseSchema):
    class Config(TaskConfig):
        schema_extra = {
            "example": {
                "title": "Task 1",
                "description": "Task 1 description",
                "status": False,
            }
        }


class TaskDBSchema(TaskBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(...)


class TaskResponseSchema(TaskDBSchema):
    class Config(TaskConfig):
        schema_extra = {
            "example": {
                "_id": "60c4b8b7e6a9d9f9f7f7f7f7",
                "title": "Task 1",
                "description": "Task 1 description",
                "status": False,
                "created_at": "2021-01-01 00:00:00",
            }
        }


class TaskListResponseSchema(BaseModel):
    tasks: list[TaskResponseSchema] = Field(...)

    class Config(TaskConfig):
        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "_id": "60c4b8b7e6a9d9f9f7f7f7f7",
                        "title": "Task 1",
                        "description": "Task 1 description",
                        "status": False,
                        "created_at": "2021-01-01 00:00:00",
                    },
                    {
                        "_id": "60c4b8b7e6a9d9f9f8f8f8f8",
                        "title": "Task 2",
                        "description": "Task 2 description",
                        "status": True,
                        "created_at": "2021-01-01 00:00:00",
                    },
                ]
            }
        }


class TaskDeleteResponseSchema(BaseModel):
    detail: str = "Task deleted successfully"
    deleted: bool = Field(...)

    class Config(TaskConfig):
        schema_extra = {
            "example": {
                "detail": "Task deleted successfully",
                "deleted": True,
            }
        }
