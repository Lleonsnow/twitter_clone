from sqlalchemy import select
from sqlalchemy.orm import Session
from tests.test_db.base_models import User
from tests.test_db.test_factories import (
    FollowerFactory,
    TweetFactory,
    UserFactory,
)


def create_user_to_db(session: Session) -> None:
    """Создание пользователя в базе данных."""
    user = UserFactory()
    session.add(user)
    session.commit()


def create_user_with_followers_to_db(session: Session) -> None:
    """Создание пользователя с подписчиками в базе данных."""
    user = UserFactory()
    follower_1 = FollowerFactory(follower=user, following=UserFactory())
    follower_2 = FollowerFactory(follower=user, following=UserFactory())
    following_1 = FollowerFactory(follower=UserFactory(), following=user)
    following_2 = FollowerFactory(follower=UserFactory(), following=user)
    user.followers.extend([follower_1, follower_2])
    user.following.extend([following_1, following_2])
    session.add(user)
    session.commit()


def create_user_with_tweets_to_db(session: Session) -> None:
    """Создание пользователя с твитами в базе данных."""
    user = UserFactory()
    tweet_1 = TweetFactory(author=user)
    tweet_2 = TweetFactory(author=user)
    user.tweets.extend([tweet_1, tweet_2])
    session.add(user)
    session.commit()


def get_user_by_id(user_id: int, session: Session) -> User | None:
    """Получение пользователя по id."""
    query = select(User).filter(User.id == user_id)
    user = session.execute(query).scalar_one_or_none()
    return user
