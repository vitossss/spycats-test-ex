import pytest
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient
from src.main import app
from sqlmodel import Session, SQLModel, create_engine
from src.routers.spycats_router import get_session


@pytest.fixture(scope="module")
def container():
    container = PostgresContainer()
    yield container.start()
    container.stop()


@pytest.fixture(scope="module")
def test_client(container):
    test_engine = create_engine(container.get_connection_url())
    SQLModel.metadata.create_all(test_engine)

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session

    return TestClient(app)
