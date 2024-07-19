from sqlalchemy import event, Engine, create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker

DATABASE_URL = "sqlite:///Test_db.db"

engine = create_engine(DATABASE_URL)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, expire_on_commit=False, autoflush=False))


def get_session() -> scoped_session:
    return session


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, *_):
    """Установка параметра pragma для async sqlite,
    дающая возможность работы с внешними ключами связанных таблиц"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
