import pytest
from app import app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture(scope="class")
def test_app(request):
    request.cls.app = app.test_client()
