from typing import BinaryIO

from sqlalchemy.orm import Session

from project_root.tests.test_db.base_models import Media


def save_media(
        file: BinaryIO,
        file_name: str,
        session: Session,
        path: str = "/home/leon/PycharmProjects/twitter_clone/project_root/tests/media/"):
    with open(f"{path}{file_name}", "wb") as f:
        f.write(file.read())
    return save_media_to_db(path, session)


def save_media_to_db(path: str, session: Session):
    media = Media(tweet_data=path)
    session.add(media)
    session.commit()
    session.refresh(media)
    return media.id
