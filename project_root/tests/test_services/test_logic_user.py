from sqlalchemy import select
from sqlalchemy.orm import Session

from project_root.tests.test_db.models import User


def get_user_from_db(user_id: int, session: Session) -> User:
    query = select(User).filter(User.id == user_id)
    user_obj = session.execute(query).scalar()
    return user_obj

