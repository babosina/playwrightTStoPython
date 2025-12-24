import pytest

from typing import Generator
from playwright.sync_api import Playwright

from utils.request_handler import RequestHandler


@pytest.fixture
def api_request(playwright: Playwright) -> Generator[RequestHandler, None, None]:
    base_url = "http://localhost:8000/api/"
    request = RequestHandler(playwright.request, base_url=base_url)
    yield request
