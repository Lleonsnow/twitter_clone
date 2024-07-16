import pytest


@pytest.mark.user
@pytest.mark.key
def test_api_key(client):
    response = client.get("/key")
    assert response.status_code == 200
    assert response.json()["name"] is not None


@pytest.mark.user
def test_user_fields(client):
    response = client.get("/user")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] is not None
    assert response_json["address"]["city"] is not None
    assert response_json["phone"] is not None
    assert response_json["email"] is not None
    assert response_json["api_key"]["name"] is not None


@pytest.mark.user
def test_user_follow(client):
    response = client.get("/user/follow")
    assert response.status_code == 200
    response_json = response.json()
    followers = response_json["followers"]
    following = response_json["following"]

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


@pytest.mark.user
def test_user_tweets(client):
    response = client.get("/user/tweets")
    assert response.status_code == 200
    response_json = response.json()
    tweets = response_json["tweets"]
    assert len(tweets) >= 2

    for tweet in tweets:
        assert tweet["content"] is not None
        assert tweet["attachments"][-1]["tweet_data"] is not None
        assert tweet["author"]["name"] is not None
        assert tweet["like_count"] >= 2
