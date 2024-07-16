import uuid

import factory
from project_root.tests.test_db.db import session
from project_root.tests.test_db.models import User, Follower, ApiKey, Tweet, Media


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = session

    id = factory.LazyAttribute(lambda _: uuid.uuid4())


class ApiKeyFactory(BaseFactory):
    class Meta:
        model = ApiKey

    name = factory.Faker("uuid4")


class MediaFactory(BaseFactory):
    class Meta:
        model = Media

    tweet_data = factory.Faker("url")
    tweet = factory.SubFactory("project_root.tests.test_db.test_factories.TweetFactory")


class TweetFactory(BaseFactory):
    class Meta:
        model = Tweet

    content = factory.Faker("sentence")
    author = factory.SubFactory("project_root.tests.test_db.test_factories.UserFactory")
    like_count = factory.Faker("random_int", min=2, max=100)
    attachments = factory.RelatedFactoryList(MediaFactory, "tweet", size=2)


class FollowerFactory(BaseFactory):
    class Meta:
        model = Follower

    follower = factory.SubFactory("project_root.tests.test_db.test_factories.UserFactory")
    following = factory.SubFactory("project_root.tests.test_db.test_factories.UserFactory")


class UserFactory(BaseFactory):
    class Meta:
        model = User

    name = factory.Faker("first_name")
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    address = factory.LazyAttribute(lambda _: {
        "id": factory.Faker("uuid4").evaluate(
            None, None, {"locale": "en_US"}),
        "street": factory.Faker("street_name").evaluate(
            None, None, {"locale": "en_US"}),
        "city": factory.Faker("city").evaluate(
            None, None, {"locale": "en_US"})
    })
    phone = factory.Faker("phone_number")
    api_key = factory.SubFactory(ApiKeyFactory)
    tweets = factory.LazyAttribute(lambda _: [])
    followers = factory.LazyAttribute(lambda _: [])
    following = factory.LazyAttribute(lambda _: [])
