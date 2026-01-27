import pytest
import os
import sys
from typing import Generator
from playwright.sync_api import Playwright
from dotenv import load_dotenv

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai_powered.utils.request_handler import RequestHandler
from ai_powered.utils.article_generator import ArticleGenerator
from utils.apilogger import APILogger
from utils.custom_expect import set_custom_api_logger

load_dotenv()

@pytest.fixture(scope="session")
def api_request(playwright: Playwright) -> Generator[RequestHandler, None, None]:
    # Ensure we use the base URL from environment or fallback to the one in yaml
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    logger = APILogger()
    set_custom_api_logger(logger)
    request_context = playwright.request.new_context()
    request = RequestHandler(request_context, base_url=base_url, logger=logger)
    yield request
    request_context.dispose()

@pytest.fixture(scope="session")
def auth_token(api_request):
    email = os.getenv("EMAIL", "pythonqa5@gmail.com")
    password = os.getenv("PASSWORD", "@$4ca*aGV$")
    
    auth_data = {
        "user": {
            "email": email,
            "password": password
        }
    }
    
    response = (api_request
                .path("/api/users/login")
                .body(auth_data)
                .post_request(200))
    
    return response["user"]["token"]

@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Token {auth_token}"}

@pytest.fixture
def article_generator():
    return ArticleGenerator()
