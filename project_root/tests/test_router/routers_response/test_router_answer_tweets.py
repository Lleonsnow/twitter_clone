from fastapi import Depends
from sqlalchemy.orm import Session
from tests.conftest import app
from tests.test_db.base_models import User
from tests.test_db.db import get_session
from tests.test_schemas.pydantic_models import BasicResponse, UserSchema
from tests.test_schemas.validators import validate_api_key
from tests.test_services.test_logic_user import (
    create_user_with_tweets_to_db,
    get_user_by_id,
)


@app.post("/user/create/tweets", response_model=BasicResponse)
def create_user_tweets(
    _: str = Depends(validate_api_key), db: Session = Depends(get_session)
) -> BasicResponse:
    """Создание пользователя с твитами."""
    create_user_with_tweets_to_db(db)
    return BasicResponse(result=True, status_code=200)


@app.get("/user/{user_id}/tweets", response_model=UserSchema)
def get_user_tweets(
    user_id: int,
    _: str = Depends(validate_api_key),
    db: Session = Depends(get_session),
) -> User:
    """Получение твитов пользователя."""
    user_tweets = get_user_by_id(user_id, db)
    return user_tweets
