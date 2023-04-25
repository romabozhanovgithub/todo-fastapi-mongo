from fastapi import HTTPException


class TaskNotFound(HTTPException):
    def __init__(self, task_id: str) -> None:
        super().__init__(status_code=404, detail=f"Task {task_id} not found")
