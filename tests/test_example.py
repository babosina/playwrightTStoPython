import re
import pytest

from typing import Any, Generator
from playwright.sync_api import Page, expect, APIRequestContext, Playwright


@pytest.mark.skip
def test_example(page: Page) -> None:
    """
    Simple navigation test
    :param page:
    :return:
    """
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))


# no recommended - invokes browser instance (Page) - slow
@pytest.mark.skip
def test_get_tags_page(page: Page) -> None:
    """
    Invokes browser instance (Page) to perform API request
    :param page:
    :return:
    """
    response = page.request.get("http://localhost:8000/api/tags")
    assert response.status == 200


# recommended - no browser context is created
@pytest.mark.skip
def test_get_tags_api_context(playwright: Playwright) -> None:
    """
    Create api context directly from playwright without invoking Page instance
    :param playwright:
    :return:
    """
    request_context: APIRequestContext = playwright.request.new_context(
        base_url="http://localhost:8000/api/"
    )
    response = request_context.get("./tags")
    assert response.ok
    print(response.json())

    request_context.dispose()


# advances approach - use context fixture
@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> Generator[APIRequestContext, Any, None]:
    context = playwright.request.new_context(
        base_url="http://localhost:8000/api/",
        extra_http_headers={
            "Accept": "application/json"
        }
    )
    yield context
    context.dispose()


@pytest.mark.skip
def test_get_tags_fixture(api_context: APIRequestContext) -> None:
    """
    Using api_context fixture
    :param api_context:
    :return:
    """
    response = api_context.get("./tags")
    assert response.ok
    data = response.json()
    assert "tags" in data
