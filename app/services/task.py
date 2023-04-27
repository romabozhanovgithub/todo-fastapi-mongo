from app.schemas.helpers import PyObjectId
from app.services.base import BaseService
from app.core.exceptions import TaskNotFound
from app.schemas import (
    TaskRequestSchema,
    TaskResponseSchema,
    TaskListResponseSchema,
)


class TaskService(BaseService):
    collection_name = "tasks"
    not_found_exception = TaskNotFound

    async def get_tasks(self) -> TaskListResponseSchema:
        tasks = await self.find_documents()
        return TaskListResponseSchema(tasks=tasks)

    async def get_tasks_by_user(
        self, user_id: str | PyObjectId
    ) -> TaskListResponseSchema:
        tasks = await self.find_documents({"user": user_id})
        return TaskListResponseSchema(tasks=tasks)

    async def get_task_by_id_and_user(
        self, task_id: str, user_id: str | PyObjectId
    ) -> TaskResponseSchema:
        task = await self.find_document_by_id(
            task_id, filter={"user": user_id}
        )
        return TaskResponseSchema(**task)

    async def create_task(self, task: dict) -> TaskResponseSchema:
        result = await self.create_document(task)
        return TaskResponseSchema(**result)

    async def update_task_by_id_and_user(
        self, task_id: str, task: TaskRequestSchema, user_id: str | PyObjectId
    ) -> TaskResponseSchema:
        result = await self.find_and_update_document_by_id(
            task_id, task.dict(), filter={"user": user_id}
        )
        return TaskResponseSchema(**result)

    async def delete_task_by_id_and_user(
        self, task_id: str, user_id: str | PyObjectId
    ) -> TaskResponseSchema:
        task = await self.find_and_delete_document_by_id(
            task_id, filter={"user": user_id}
        )
        return TaskResponseSchema(**task)
