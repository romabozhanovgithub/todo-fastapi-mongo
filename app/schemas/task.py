from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field

from app.schemas import PyObjectId

schema_extra = {
    "example": {
        "title": "Task 1",
        "description": "Task 1 description",
        "status": False,
        "created_at": "2021-01-01 00:00:00"
    }
}


class TaskConfig:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {
        ObjectId: str
    }


class TaskBaseSchema(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    status: bool = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TaskRequestSchema(TaskBaseSchema):
    class Config(TaskConfig):
        schema_extra = schema_extra


class TaskResponseSchema(TaskBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config(TaskConfig):
        schema_extra = schema_extra.update(
            {
                "example": {
                    "id": "5ff4f9c9e4b0e8b9b8e9f9f9",
                    **schema_extra["example"]
                }
            }
        )
