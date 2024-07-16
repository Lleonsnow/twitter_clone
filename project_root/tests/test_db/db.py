from sqlalchemy import event, Engine, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from project_root.tests.test_db.models import Base

DATABASE_URL = "sqlite:///Test_db.db"

engine = create_engine(
    DATABASE_URL, echo=True)
session = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, *_):
    """Установка параметра pragma для async sqlite,
    дающая возможность работы с внешними ключами связанных таблиц"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
