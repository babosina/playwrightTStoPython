import pytest
import os
import random
import string
from playwright.sync_api import Page, expect


@pytest.fixture
def random_user():
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        "username": f"user_{random_str}",
        "email": f"user_{random_str}@example.com",
        "password": "Password123!"
    }


@pytest.fixture(autouse=True)
def setup(page: Page):
    base_url = os.getenv("UI_BASE_URL", "http://localhost:4200/#/")
    page.goto(base_url)


def pytest_runtest_makereport(item, call):
    if call.when == 'call' and call.excinfo is not None:
        page = item.funcargs.get('page')
        if page:
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            # Ensure the test name is safe for a filename
            test_name = item.name.replace("[", "_").replace("]", "_").replace("/", "_")
            page.screenshot(path=f"screenshots/{test_name}.png")
