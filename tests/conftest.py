import pytest
import requests_mock

@pytest.fixture
def mock_requests():
    """Provides a requests-mock fixture for testing HTTP requests."""
    with requests_mock.Mocker() as m:
        yield m