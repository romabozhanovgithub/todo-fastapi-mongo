from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, detail: str, status_code: int = 404) -> None:
        super().__init__(status_code=status_code, detail=detail)


class TaskNotFound(BaseHTTPException):
    def __init__(self, task_id: str, status_code=404) -> None:
        super().__init__(
            status_code=status_code, detail=f"Task {task_id} not found"
        )
