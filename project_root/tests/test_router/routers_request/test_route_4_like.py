import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.like
def test_post_user_like(client: TestClient, db: Session) -> None:
    """Тест создания лайка."""
    response = client.post("/tweets/1/likes", headers={"api-key": "test"})
    assert response.status_code == 200
    resp_object = response.json()
    assert resp_object["result"] is True


@pytest.mark.like
def test_post_user_unlike(client: TestClient, db: Session) -> None:
    """Тест удаления лайка."""
    response = client.post("/tweets/1/likes", headers={"api-key": "test"})
    assert response.status_code == 200
    resp_object = response.json()
    assert resp_object["result"] is True
