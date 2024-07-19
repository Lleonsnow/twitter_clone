import pytest
from fastapi.testclient import TestClient
from project_root.tests.test_db.db import session, engine
from project_root.tests.test_db.base_models import Base
from fastapi import FastAPI

app = FastAPI()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def db(create_test_db):
    yield session


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
