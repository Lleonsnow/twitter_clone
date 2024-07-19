import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.tweet
def test_post_user_tweets(client: TestClient, db: Session) -> None:
    response = client.post("/user/create/tweets", headers={"api-key": "test"})
    assert response.status_code == 200
    resp_object = response.json()
    assert resp_object["result"] is True


@pytest.mark.tweet
def test_get_user_tweets(client: TestClient, db: Session) -> None:
    response = client.get("/user/7/tweets", headers={"api-key": "test"})
    assert response.status_code == 200
    resp_object = response.json()
    tweets = resp_object["tweets"]
    assert len(tweets) == 2

    for tweet in tweets:
        assert tweet["content"] is not None
        assert tweet["author"]["name"] is not None
        assert tweet["like_count"] == len(tweet["likes"])
        assert tweet["likes"][-1]["name"] is not None
        assert tweet["attachments"][-1]["tweet_data"] is not None


