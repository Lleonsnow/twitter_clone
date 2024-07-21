from typing import BinaryIO

from sqlalchemy.orm import Session
from tests.test_db.base_models import Media


def save_media(
    file: BinaryIO,
    file_name: str,
    session: Session,
    path: str = "/tests/media/",
):
    """Сохраняет медиа-файл локально."""
    with open(f"{path}{file_name}", "wb") as f:
        f.write(file.read())
    return save_media_to_db(path, session)


def save_media_to_db(path: str, session: Session):
    """Создает объект медиа-файла в базе данных и возвращает его id."""
    media = Media(tweet_data=path)
    session.add(media)
    session.commit()
    session.refresh(media)
    return media.id
