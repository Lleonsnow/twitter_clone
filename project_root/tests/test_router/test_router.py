from project_root.tests.test_main import app
from project_root.tests.test_db.test_factories import UserFactory, ApiKeyFactory, FollowerFactory, TweetFactory
from project_root.tests.test_schemas.pydantic_models import UserSchema, ApiKeySchema, SimplifiedUserSchema, TweetSchema


@app.get("/key", response_model=ApiKeySchema)
def get_key():
    api_key = ApiKeyFactory()
    return api_key


@app.get("/user", response_model=SimplifiedUserSchema)
def get_user():
    user = UserFactory()
    return user


@app.get("/user/follow", response_model=UserSchema)
def get_user_follow():
    user = UserFactory()
    follower_1 = FollowerFactory(follower=user, following=UserFactory())
    follower_2 = FollowerFactory(follower=user, following=UserFactory())
    following_1 = FollowerFactory(follower=UserFactory(), following=user)
    following_2 = FollowerFactory(follower=UserFactory(), following=user)
    user.followers.extend([follower_1, follower_2])
    user.following.extend([following_1, following_2])

    return user


@app.get("/user/tweets", response_model=UserSchema)
def get_user_tweets():
    user = UserFactory()
    tweet_1 = TweetFactory(author=user)
    tweet_2 = TweetFactory(author=user)
    user.tweets.extend([tweet_1, tweet_2])

    return user
