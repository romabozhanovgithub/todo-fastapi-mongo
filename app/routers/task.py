from fastapi import APIRouter, Depends

from app.services import TaskService
from app.schemas import TaskRequestSchema, TaskResponseSchema, TaskListResponseSchema, TaskDeleteResponseSchema
from app.core.exceptions import TaskNotFound
from app.core.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=TaskListResponseSchema)
async def get_tasks(
    task_service: TaskService = Depends(get_task_service),
) -> TaskListResponseSchema:
    tasks = await task_service.get_tasks()
    return tasks


@router.get("/{task_id}", response_model=TaskResponseSchema)
async def get_task(
    task_id: str, task_service: TaskService = Depends(get_task_service)
) -> TaskResponseSchema:
    task = await task_service.get_task(task_id)
    if not task:
        raise TaskNotFound(task_id)
    return task


@router.post("/", response_model=TaskResponseSchema)
async def create_task(
    task: TaskRequestSchema, task_service: TaskService = Depends(get_task_service)
) -> TaskResponseSchema:
    task = await task_service.create_task(task)
    return task


@router.put("/{task_id}", response_model=TaskResponseSchema)
async def update_task(
    task_id: str,
    task: TaskRequestSchema,
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponseSchema:
    task = await task_service.update_task(task_id, task)
    if not task:
        raise TaskNotFound(task_id)
    return task


@router.delete("/{task_id}", response_model=TaskDeleteResponseSchema)
async def delete_task(
    task_id: str, task_service: TaskService = Depends(get_task_service)
) -> TaskDeleteResponseSchema:
    deleted = await task_service.delete_task(task_id)
    if not deleted:
        raise TaskNotFound(task_id)
    return {
        "deleted": deleted,
    }
