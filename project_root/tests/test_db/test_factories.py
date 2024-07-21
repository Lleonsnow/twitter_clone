import factory
from tests.test_db.base_models import (
    ApiKey,
    Follower,
    Like,
    Media,
    Tweet,
    User,
)
from tests.test_db.db import session


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Базовая фабрика."""

    class Meta:
        sqlalchemy_session = session


class ApiKeyFactory(BaseFactory):
    """Фабрика API ключа."""

    class Meta:
        model = ApiKey

    name = factory.Faker("uuid4")


class MediaFactory(BaseFactory):
    """Фабрика медиафайла."""

    class Meta:
        model = Media

    tweet_data = factory.Faker("url")
    tweet = factory.SubFactory("tests.test_db.test_factories.TweetFactory")


class LikeFactory(BaseFactory):
    """Фабрика лайка."""

    class Meta:
        model = Like

    name = factory.Faker("user_name")
    tweet = factory.SubFactory("tests.test_db.test_factories.TweetFactory")
    user = factory.SubFactory("tests.test_db.test_factories.UserFactory")


class TweetFactory(BaseFactory):
    """Фабрика твита."""

    class Meta:
        model = Tweet

    content = factory.Faker("sentence")
    author = factory.SubFactory("tests.test_db.test_factories.UserFactory")
    like_count = factory.Faker("random_int", min=10, max=10)
    likes = factory.RelatedFactoryList(LikeFactory, "tweet", size=10)
    attachments = factory.RelatedFactoryList(MediaFactory, "tweet", size=2)


class FollowerFactory(BaseFactory):
    """Фабрика подписчика."""

    class Meta:
        model = Follower

    follower = factory.SubFactory(
        "tests.test_db.test_factories.UserFactory"
    )
    following = factory.SubFactory(
        "tests.test_db.test_factories.UserFactory"
    )


class UserFactory(BaseFactory):
    """Фабрика пользователя."""

    class Meta:
        model = User

    name = factory.Faker("first_name")
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    address = factory.LazyAttribute(
        lambda _: {
            "id": factory.Faker("uuid4").evaluate(
                None, None, {"locale": "en_US"}
            ),
            "street": factory.Faker("street_name").evaluate(
                None, None, {"locale": "en_US"}
            ),
            "city": factory.Faker("city").evaluate(
                None, None, {"locale": "en_US"}
            ),
        }
    )
    phone = factory.Faker("phone_number")
    api_key = factory.SubFactory(ApiKeyFactory)
    tweets = factory.LazyAttribute(lambda _: [])
    likes = factory.LazyAttribute(lambda _: [])
    followers = factory.LazyAttribute(lambda _: [])
    following = factory.LazyAttribute(lambda _: [])
