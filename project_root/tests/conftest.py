import pytest
from fastapi.testclient import TestClient
from project_root.tests.test_main import app
from project_root.tests.test_db.db import session


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db():
    return session
