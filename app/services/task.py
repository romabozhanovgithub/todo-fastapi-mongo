from datetime import datetime

from app.services.base import BaseService
from app.core.exceptions import TaskNotFound
from app.schemas import (
    TaskRequestSchema,
    TaskResponseSchema,
    TaskListResponseSchema,
)


class TaskService(BaseService):
    collection_name = "tasks"
    not_found_error = TaskNotFound

    async def get_tasks(self) -> TaskListResponseSchema:
        tasks = await self.collection.find().to_list(length=100)
        return tasks

    async def get_task(self, task_id: str) -> TaskResponseSchema:
        task = await self.collection.find_one({"_id": self._get_id(task_id)})
        return task

    async def create_task(self, task: TaskRequestSchema) -> TaskResponseSchema:
        result = await self.collection.insert_one(
            {**task.dict(), "created_at": datetime.utcnow()}
        )
        new_task = await self.get_task(result.inserted_id)
        return new_task

    async def update_task(
        self, task_id: str, task: TaskRequestSchema
    ) -> TaskResponseSchema:
        await self.collection.update_one(
            {"_id": self._get_id(task_id)}, {"$set": task.dict()}
        )
        new_task = await self.get_task(task_id)
        return new_task

    async def delete_task(self, task_id: str) -> bool:
        await self.collection.delete_one({"_id": self._get_id(task_id)})
        return True
