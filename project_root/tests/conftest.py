import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tests.test_db.base_models import Base
from tests.test_db.db import engine, session

app = FastAPI()


@pytest.fixture
def client():
    """Пробрасывание клиента для тестирования."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def db(create_test_db):
    """Пробрасывание сессии для тестирования."""
    yield session


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """Создание тестовой базы данных."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
