from sqlalchemy import delete
from sqlalchemy.orm import Session
from tests.test_db.base_models import Follower, User
from tests.test_db.test_factories import FollowerFactory
from tests.test_services.test_logic_user import get_user_by_id


def post_follower_by_id(
    follower_id: int, following_id: int, db: Session
) -> User:
    """Подписка на пользователя."""
    user_follower = get_user_by_id(follower_id, db)
    user_following = get_user_by_id(following_id, db)
    follower = FollowerFactory(
        follower=user_follower, following=user_following
    )
    user_follower.following.append(follower)
    user_following.followers.append(follower)
    db.add(follower)
    db.commit()
    db.refresh(user_follower)
    return user_follower


def delete_follower_by_id(
    follower_id: int, following_id: int, db: Session
) -> User:
    """Подписка на пользователя."""
    query = delete(Follower).filter(
        Follower.follower_id == follower_id,
        Follower.following_id == following_id,
    )
    db.execute(query)
    db.commit()
    user_follower = get_user_by_id(follower_id, db)
    return user_follower
