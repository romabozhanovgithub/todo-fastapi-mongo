import pytest

from app.services.task import TaskService


@pytest.mark.asyncio
async def test_get_tasks_with_existing_task(
    task_service: TaskService, task_data_with_user: dict
):
    new_task = await task_service.create_task(task_data_with_user)
    found_task = await task_service.get_tasks()
    assert len(found_task.tasks) > 0


@pytest.mark.asyncio
async def test_get_task_by_id_and_user(
    task_service: TaskService, task_data_with_user: dict
):
    new_task = await task_service.create_task(task_data_with_user)
    found_task = await task_service.get_task_by_id_and_user(
        new_task.id, task_data_with_user["user"]
    )
    assert found_task.user == task_data_with_user["user"]
    assert found_task.created_at is not None


@pytest.mark.asyncio
async def test_get_task_by_id_and_user_not_found(
    task_service: TaskService, task_data_with_user: dict
):
    new_task = await task_service.create_task(task_data_with_user)
    with pytest.raises(task_service.not_found_exception):
        await task_service.get_task_by_id_and_user(new_task.id, "invalid")


@pytest.mark.asyncio
async def test_create_task(task_service: TaskService, task_data: dict):
    new_task = await task_service.create_task(task_data)
    assert new_task.title == task_data["title"]
    assert new_task.created_at is not None


@pytest.mark.asyncio
async def test_update_task_by_id_and_user(
    task_service: TaskService, task_data_with_user: dict
):
    new_task = await task_service.create_task(task_data_with_user)
    updated_task = await task_service.update_task_by_id_and_user(
        new_task.id, {"title": "updated"}, task_data_with_user["user"]
    )
    assert updated_task.title == "updated"
    assert updated_task.created_at is not None


@pytest.mark.asyncio
async def test_update_task_by_id_and_user_not_found(
    task_service: TaskService, task_data_with_user: dict
):
    new_task = await task_service.create_task(task_data_with_user)
    with pytest.raises(task_service.not_found_exception):
        await task_service.update_task_by_id_and_user(
            new_task.id, {"title": "updated"}, "invalid"
        )


@pytest.mark.asyncio
async def test_delete_task_by_id_and_user(
    task_service: TaskService, task_data_with_user: dict
):
    new_task = await task_service.create_task(task_data_with_user)
    deleted_task = await task_service.delete_task_by_id_and_user(
        str(new_task.id), task_data_with_user["user"]
    )
    assert deleted_task.title == task_data_with_user["title"]
    assert deleted_task.created_at is not None


@pytest.mark.asyncio
async def test_delete_task_by_id_and_user_not_found(
    task_service: TaskService, task_data_with_user: dict
):
    new_task = await task_service.create_task(task_data_with_user)
    with pytest.raises(task_service.not_found_exception):
        await task_service.delete_task_by_id_and_user(
            str(new_task.id), "invalid"
        )
