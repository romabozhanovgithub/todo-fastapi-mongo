from datetime import datetime
from bson import ObjectId

from app.services import BaseService
from app.schemas import TaskDBSchema, TaskRequestSchema


class TaskService(BaseService):
    collection_name = "tasks"

    async def get_tasks(self) -> list[TaskDBSchema]:
        tasks = await self.collection.find().to_list(length=100)
        return tasks

    async def get_task(self, task_id: str) -> TaskDBSchema:
        task = await self.collection.find_one({"_id": ObjectId(task_id)})
        return task

    async def create_task(self, task: TaskRequestSchema) -> TaskDBSchema:
        new_task = task.dict()
        new_task["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(new_task)
        task = await self.get_task(result.inserted_id)
        return task

    async def update_task(
        self, task_id: str, task: TaskRequestSchema
    ) -> TaskDBSchema:
        await self.collection.update_one(
            {"_id": ObjectId(task_id)}, {"$set": task.dict()}
        )
        task = await self.get_task(task_id)
        return task

    async def delete_task(self, task_id: str) -> bool:
        try:
            await self.collection.delete_one({"_id": ObjectId(task_id)})
            return True
        except Exception as e:
            print(e)
            return False
