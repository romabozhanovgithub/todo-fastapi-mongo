from fastapi import APIRouter, Depends, status

from app.services import TaskService
from app.schemas import (
    TaskRequestSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
    TaskListResponseSchema,
    TaskDeleteResponseSchema,
    TaskNotFoundResponseSchema,
    UserDBBaseSchema,
)
from app.core.dependencies import get_request_user, get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/",
    summary="List of tasks",
    response_model=TaskListResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    task_service: TaskService = Depends(get_task_service),
    user: UserDBBaseSchema = Depends(get_request_user),
) -> TaskListResponseSchema:
    tasks = await task_service.get_tasks_by_user(user.id)
    return tasks


@router.get(
    "/{task_id}",
    summary="Get task by ID",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": TaskNotFoundResponseSchema}},
)
async def get_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
    user: UserDBBaseSchema = Depends(get_request_user),
) -> TaskResponseSchema:
    task = await task_service.get_task_by_id_and_user(task_id, user.id)
    return task


@router.post(
    "/",
    summary="Create new task",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: TaskRequestSchema,
    task_service: TaskService = Depends(get_task_service),
    user: UserDBBaseSchema = Depends(get_request_user),
) -> TaskResponseSchema:
    new_task = await task_service.create_task({**task.dict(), "user": user.id})
    return new_task


@router.put(
    "/{task_id}",
    summary="Update task",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": TaskNotFoundResponseSchema}},
)
async def update_task(
    task_id: str,
    task: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service),
    user: UserDBBaseSchema = Depends(get_request_user),
) -> TaskResponseSchema:
    updated_task = await task_service.update_task_by_id_and_user(
        task_id, task.dict(exclude_none=True), user.id
    )
    return updated_task


@router.delete(
    "/{task_id}",
    summary="Delete task",
    response_model=TaskDeleteResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": TaskNotFoundResponseSchema}},
)
async def delete_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
    user: UserDBBaseSchema = Depends(get_request_user),
) -> TaskDeleteResponseSchema:
    task = await task_service.delete_task_by_id_and_user(task_id, user.id)
    return TaskDeleteResponseSchema(
        message=f"Task with id {task_id} has been deleted", task=task
    )
