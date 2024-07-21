import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.user
def test_user_object_after_create(client: TestClient, db: Session) -> None:
    """Тест создания пользователя."""
    response = client.post("/user/me", headers={"api-key": "test"})
    assert response.status_code == 200
    resp_object = response.json()
    assert resp_object["result"] is True


@pytest.mark.user
def test_user_get_by_id(client: TestClient, db: Session) -> None:
    """Тест получения пользователя по id."""
    response = client.get("/user/1", headers={"api-key": "test"})
    assert response.status_code == 200
    resp_object = response.json()
    assert resp_object["name"] is not None
    assert resp_object["address"]["city"] is not None
    assert resp_object["phone"] is not None
    assert resp_object["email"] is not None
    assert resp_object["api_key"]["name"] is not None
    assert resp_object["tweets"] == []
    assert resp_object["likes"] == []
    assert resp_object["followers"] == []


@pytest.mark.xfail
def test_user_get_by_id_2(client: TestClient, db: Session) -> None:
    """Тест получения пользователя по id."""
    response = client.get("/user/2", headers={"api-key": "test"})
    assert response.status_code == 200
