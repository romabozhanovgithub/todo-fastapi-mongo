from fastapi import status
from fastapi.testclient import TestClient
from app.main import app


def test_login(user_in_db, user_data):
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            data={
                "username": user_in_db.email,
                "password": user_data["password"],
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["access_token"]


def test_login_with_wrong_credentials(user_in_db):
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            data={
                "username": user_in_db.email,
                "password": "wrong_password",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_signup():
    with TestClient(app) as client:
        user_data = {
            "full_name": "test_name",
            "email": "test_email@gmail.com",
            "password": "test_password",
        }
        response = client.post(
            "/auth/signup",
            json=user_data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == user_data["email"]


def test_signup_with_existing_user(user_data, user_in_db):
    with TestClient(app) as client:
        response = client.post(
            "/auth/signup",
            json=user_data,
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "User already exists"


def test_signup_with_wrong_email(user_data):
    user_data["email"] = "wrong_email"
    with TestClient(app) as client:
        response = client.post(
            "/auth/signup",
            json=user_data,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (
            response.json()["detail"][0]["msg"]
            == "value is not a valid email address"
        )
