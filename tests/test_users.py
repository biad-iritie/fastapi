
import json
from jose import jwt
from app.main import app
from app import schemas
from app.config import settings
# if i want to use alembic
from alembic import command
import pytest


""" def test_root(client):
    res = client.get("/")
    print(res.json())
 """


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "pytest@gmail.com",
                         "password": "1234"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "pytest@gmail.com"
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password,status_code", [
    ("wrong@gmail.com", "admin", 403),
    ("pytest@gmail.com", "wrong", 403),
    ("wrong@gmail.com", "wrong", 403),
    (None, "admin", 422),
    ("pytest@gmail.com", None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })
    assert res.status_code == status_code
    #assert res.json().get("detail") == "Invalid Credentials"
