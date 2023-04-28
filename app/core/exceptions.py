from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, detail: str, status_code: int = 404) -> None:
        super().__init__(status_code=status_code, detail=detail)


class TaskNotFound(BaseHTTPException):
    def __init__(self, task_id: str, status_code=404) -> None:
        super().__init__(
            status_code=status_code, detail=f"Task {task_id} not found"
        )


class UserNotFound(BaseHTTPException):
    def __init__(self, user_id: str, status_code=404) -> None:
        super().__init__(
            status_code=status_code, detail=f"User {user_id} not found"
        )


class UserAlreadyExists(BaseHTTPException):
    def __init__(self, status_code=409) -> None:
        super().__init__(status_code=status_code, detail="User already exists")


class UserInvalidCredentials(BaseHTTPException):
    def __init__(self, status_code=401) -> None:
        super().__init__(status_code=status_code, detail="Invalid credentials")
