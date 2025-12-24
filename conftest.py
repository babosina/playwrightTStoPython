import pytest
import os

from dotenv import load_dotenv
from typing import Generator
from playwright.sync_api import Playwright

from utils.request_handler import RequestHandler

load_dotenv()


@pytest.fixture
def api_request(playwright: Playwright) -> Generator[RequestHandler, None, None]:
    base_url = "http://localhost:8000/api/"
    request_context = playwright.request.new_context()
    request = RequestHandler(request_context, base_url=base_url)
    yield request
    request_context.dispose()


@pytest.fixture
def get_token(api_request):
    print("TOKEN FIXTURE")
    auth_data = {
        "user": {
            "password": os.getenv("PASSWORD"),
            "email": os.getenv("EMAIL")
        }
    }
    token_response = (api_request
                      .path("./users/login")
                      .body(auth_data)
                      .post_request(200))
    token = token_response.get("user").get("token")
    yield token
