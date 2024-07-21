from fastapi import Depends
from sqlalchemy.orm import Session
from tests.conftest import app
from tests.test_db.base_models import User
from tests.test_db.db import get_session
from tests.test_schemas.pydantic_models import BasicResponse, UserSchema
from tests.test_schemas.validators import validate_api_key
from tests.test_services.test_logic_follower import (
    delete_follower_by_id,
    post_follower_by_id,
)
from tests.test_services.test_logic_user import (
    create_user_with_followers_to_db,
    get_user_by_id,
)


@app.post("/user/create/follow", response_model=BasicResponse)
def create_user_follow(
    db: Session = Depends(get_session),
) -> BasicResponse:
    """Создание пользователя с подписками."""
    create_user_with_followers_to_db(db)
    return BasicResponse(result=True, status_code=200)


@app.get("/user/{user_id}/followers", response_model=UserSchema)
def route_get_user_followers_by_id(
    user_id: int,
    _: str = Depends(validate_api_key),
    db: Session = Depends(get_session),
) -> User:
    """Получение подписок пользователя."""
    user = get_user_by_id(user_id, db)
    return user


@app.post(
    "/user/{follower_id}/follow/{following_id}", response_model=UserSchema
)
def route_post_user_follower_by_id(
    follower_id: int,
    following_id: int,
    _: str = Depends(validate_api_key),
    db: Session = Depends(get_session),
) -> User:
    """Подписка на пользователя."""
    user = post_follower_by_id(follower_id, following_id, db)
    return user


@app.delete(
    "/user/{follower_id}/follow/{following_id}", response_model=UserSchema
)
def route_delete_user_follower_by_id(
    follower_id: int,
    following_id: int,
    _: str = Depends(validate_api_key),
    db: Session = Depends(get_session),
) -> User:
    """Отписка от пользователя."""
    user = delete_follower_by_id(follower_id, following_id, db)
    return user
