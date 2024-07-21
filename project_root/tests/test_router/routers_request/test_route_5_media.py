import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.media
def test_post_user_media(client: TestClient, db: Session) -> None:
    """Тест сохранения медиафайла в базу данных."""
    path = (
        "/".join(os.path.abspath(__file__).split(os.sep)[:-3])
        + "/media/1.jpg"
    )
    with open(path, "rb") as file:
        response = client.post(
            "/medias",
            headers={"api-key": "test"},
            files={"file": ("1.jpg", file, "image/png")},
        )
    assert response.status_code == 200
    resp_object = response.json()
    assert resp_object["result"] is True
    assert resp_object["media_id"] == 5


# @pytest.mark.media
# def test_get_media_by_id(client: TestClient) -> None:
#     """Тест получения медиафайла."""
#     path = (
#         "/".join(os.path.abspath(__file__).split(os.sep)[:-3])
#         + "/media/1.jpg"
#     )
#     response = client.get(path, headers={"api-key": "test"})
#     assert response.status_code == 200
#     assert response.headers["content-type"] == "image/png"
#     with open(path, "rb") as media_file:
#         assert response.content == media_file.read()
