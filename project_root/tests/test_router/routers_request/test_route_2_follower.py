import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.follower
def test_post_user_follow(client: TestClient, db: Session) -> None:
    response = client.post("/user/create/follow", headers={"api-key": "test"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["result"] is True


@pytest.mark.follower
def test_get_user_followers(client: TestClient, db: Session) -> None:
    response = client.get("/user/2/followers", headers={"api-key": "test"})
    assert response.status_code == 200
    resp_object = response.json()
    followers = resp_object["followers"]
    following = resp_object["following"]

    assert len(followers) == len(following) == 2

    for follower in followers:
        assert follower["follower"]["name"] is not None
        assert follower["follower"]["address"]["city"] is not None
        assert follower["follower"]["phone"] is not None
        assert follower["follower"]["email"] is not None
        assert follower["follower"]["api_key"]["name"] is not None

    for following in following:
        assert following["following"]["name"] is not None
        assert following["following"]["address"]["city"] is not None
        assert following["following"]["phone"] is not None
        assert following["following"]["email"] is not None
        assert following["following"]["api_key"]["name"] is not None
