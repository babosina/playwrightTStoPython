import pytest
import os

from dotenv import load_dotenv
from typing import Generator
from playwright.sync_api import Playwright

from utils.apilogger import APILogger
from utils.request_handler import RequestHandler
from utils.custom_expect import set_custom_api_logger

load_dotenv()


@pytest.fixture
def api_request(playwright: Playwright) -> Generator[RequestHandler, None, None]:
    base_url = os.getenv("BASE_URL")
    logger = APILogger()
    set_custom_api_logger(logger)
    request_context = playwright.request.new_context()
    request = RequestHandler(request_context, base_url=base_url, logger=logger)
    yield request
    request_context.dispose()


@pytest.fixture
def get_token(api_request):
    auth_data = {
        "user": {
            "password": os.getenv("PASSWORD"),
            "email": os.getenv("EMAIL")
        }
    }
    try:
        token_response = (api_request
                          .path("./users/login")
                          .body(auth_data)
                          .post_request(200))
        token = token_response.get("user").get("token")
        yield token
    except RuntimeError as e:
        raise RuntimeError(f"Failed to obtain token: {e}")


# An example of a fixture to orchestrate test configuration
# Determine environment
test_env = os.getenv('TEST_ENV', 'dev')
print(f"Running test in {test_env} environment")


class Config:
    """Test configuration class"""
    api_url: str = os.getenv('BASE_URL', '')
    user_email: str = os.getenv('EMAIL', '')
    user_password: str = os.getenv('PASSWORD', '')


# Override config based on an environment
if test_env == 'qa':
    Config.user_email = os.getenv('EMAIL', '')
    Config.user_password = os.getenv('PASSWORD', '')


@pytest.fixture(scope='session')
def config():
    """Pytest fixture that provides test configuration"""
    return Config()


@pytest.fixture(scope='session')
def api_url():
    """Pytest fixture that provides API URL"""
    return Config.api_url


@pytest.fixture(scope='session')
def user_credentials():
    """Pytest fixture that provides user credentials"""
    return {
        'email': Config.user_email,
        'password': Config.user_password
    }
