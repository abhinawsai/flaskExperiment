import pytest
import app

@pytest.fixture
def test():
    test = app()
    yield test

@pytest.fixture
def client(test):
    return test.test_client()
