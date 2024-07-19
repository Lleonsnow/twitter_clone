from fastapi.responses import JSONResponse
from sqlalchemy import delete
from sqlalchemy.orm import Session
from http import HTTPStatus


from project_root.tests.test_db.base_models import Like, User
from project_root.tests.test_services.test_logic_tweet import get_tweet_by_id
from project_root.tests.test_services.test_logic_user import get_user_by_id
from project_root.tests.exceptions.error_handler import error_handler
from project_root.tests.exceptions.models import TweetNotFound
from project_root.tests.test_schemas.pydantic_models import ErrorResponse


def set_user_like_to_db(tweet_id: int, db: Session) -> ErrorResponse | None:
    tweet = get_tweet_by_id(tweet_id, db)
    if not tweet:
        return error_handler(TweetNotFound(message="Tweet not found", status=HTTPStatus.NOT_FOUND))
    user = get_user_by_id(1, db)
    like = Like(tweet=tweet, user=user, name=user.name)
    tweet.like_count += 1
    db.add(like)
    db.commit()


def set_user_unlike_to_db(tweet_id: int, db: Session) -> ErrorResponse | None:
    tweet = get_tweet_by_id(tweet_id, db)
    if not tweet:
        return error_handler(TweetNotFound(message="Tweet not found", status=HTTPStatus.NOT_FOUND))
    like = delete(Like).filter(Like.tweet_id == tweet_id)
    tweet.like_count -= 1
    db.delete(like)
    db.commit()
