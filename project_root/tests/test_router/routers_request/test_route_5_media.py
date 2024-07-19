import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.media
def test_post_user_media(client: TestClient, db: Session) -> None:
    path = "/home/leon/PycharmProjects/twitter_clone/project_root/tests/media/"
    with open(f"{path}1.jpg", "rb") as file:
        response = client.post("/medias",
                               headers={"api-key": "test"},
                               files={"file": ("1.jpg", file, "image/png")})
    assert response.status_code == 200
    resp_object = response.json()
    assert resp_object["result"] is True
    assert resp_object["media_id"] == 5
