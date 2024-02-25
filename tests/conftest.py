import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# from core.config import AppSettings
from src.main import app

# class TestAppSettings(AppSettings):
#     database_dsn: str = "test database string"
#     database_dsn: str = "1234"


# @pytest.fixture(autouse=True, scope="session")
# def test_settings(monkeypatch):
#     environ["DATABASE_DSN"] = "test database string"
#     environ["EXCHANGE_RATE_API_KEY"] = "1234"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/ratevid",
        echo=True,
        future=True,
    )
    with Session(engine) as session:
        yield session
