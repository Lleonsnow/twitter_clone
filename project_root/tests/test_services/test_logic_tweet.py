from sqlalchemy import select
from sqlalchemy.orm import Session
from tests.test_db.base_models import Tweet


def get_tweet_by_id(tweet_id: int, session: Session) -> Tweet | None:
    """Получение твита по id."""
    query = select(Tweet).filter(Tweet.id == tweet_id)
    tweet = session.execute(query).scalar_one_or_none()
    return tweet
