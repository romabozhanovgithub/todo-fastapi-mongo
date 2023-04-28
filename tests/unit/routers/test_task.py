from fastapi import status
from fastapi.testclient import TestClient
from app.main import app


def test_get_tasks(auth_token, task_in_db):
    with TestClient(app) as client:
        response = client.get(
            "/tasks/",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json()["tasks"], list)
        assert response.json()["tasks"][0]["_id"] == str(task_in_db.id)


def test_get_tasks_with_wrong_token():
    with TestClient(app) as client:
        response = client.get(
            "/tasks/",
            headers={"Authorization": "Bearer wrong_token"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_task(auth_token, task_in_db):
    with TestClient(app) as client:
        response = client.get(
            f"/tasks/{task_in_db.id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["_id"] == str(task_in_db.id)


def test_get_task_with_wrong_token(task_in_db):
    with TestClient(app) as client:
        response = client.get(
            f"/tasks/{task_in_db.id}",
            headers={"Authorization": "Bearer wrong_token"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_task_with_wrong_id(auth_token):
    with TestClient(app) as client:
        response = client.get(
            "/tasks/wrong_id",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_task(auth_token, user_in_db, task_data):
    with TestClient(app) as client:
        response = client.post(
            "/tasks/",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=task_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["title"] == task_data["title"]
        assert response.json()["description"] == task_data["description"]
        assert response.json()["user"] == str(user_in_db.id)


def test_create_task_with_wrong_token(task_data):
    with TestClient(app) as client:
        response = client.post(
            "/tasks/",
            headers={"Authorization": "Bearer wrong_token"},
            json=task_data,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_task_with_wrong_data(auth_token):
    with TestClient(app) as client:
        response = client.post(
            "/tasks/",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"title": "test"},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_task(auth_token, task_in_db):
    with TestClient(app) as client:
        response = client.put(
            f"/tasks/{str(task_in_db.id)}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"title": "new_title"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "new_title"


def test_update_task_with_wrong_token(task_in_db):
    with TestClient(app) as client:
        response = client.put(
            f"/tasks/{str(task_in_db.id)}",
            headers={"Authorization": "Bearer wrong_token"},
            json={"title": "new_title"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_task_with_wrong_id(auth_token):
    with TestClient(app) as client:
        response = client.put(
            "/tasks/wrong_id",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"title": "new_title"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task(auth_token, task_in_db):
    with TestClient(app) as client:
        response = client.delete(
            f"/tasks/{str(task_in_db.id)}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        task_response = client.get(
            f"/tasks/{str(task_in_db.id)}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert task_response.status_code == status.HTTP_404_NOT_FOUND
        assert response.status_code == status.HTTP_200_OK


def test_delete_task_with_wrong_token(task_in_db):
    with TestClient(app) as client:
        response = client.delete(
            f"/tasks/{str(task_in_db.id)}",
            headers={"Authorization": "Bearer wrong_token"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_task_with_wrong_id(auth_token):
    with TestClient(app) as client:
        response = client.delete(
            "/tasks/wrong_id",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
