import pytest

from typing import Any, Generator
from playwright.sync_api import Page, expect, APIRequestContext, Playwright, APIResponse


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


def test_get_all_tags(api_context: APIRequestContext) -> None:
    response = api_context.get("./tags")
    response_json = response.json()
    assert response_json.get("tags")[0] == "django"
    assert len(response_json.get("tags")) >= 5


def test_get_all_articles(api_context: APIRequestContext) -> None:
    response = api_context.get("./articles")
    assert response.ok
    assert len(response.json().get("articles")) >= 3
    assert response.json().get("articlesCount") == 5


def test_create_article(api_context: APIRequestContext) -> None:
    data = {
        "user": {
            "password": "@$4ca*aGV$",
            "email": "pythonqa5@gmail.com"
        }
    }
    token_response: APIResponse = api_context.post("./users/login", data=data)
    token = token_response.json().get("user").get("token")

    new_article_data = {
        "article": {
            "title": "Testing APIs with Playwright from Code",
            "description": "Amazing features",
            "body": "Come use Postman for the API testing with us!",
            "tagList": [
                "Playwright"
            ]
        }
    }

    create_article_response: APIResponse = api_context.post("./articles",
                                                            headers={"Authorization": f"Token {token}"},
                                                            data=new_article_data)
    assert create_article_response.ok
    assert create_article_response.json().get("article").get("title") == "Testing APIs with Playwright from Code"
    assert create_article_response.json().get("article").get("tagList") == ["Playwright"]

    get_articles_response: APIResponse = api_context.get("./articles",
                                                         headers={"Authorization": f"Token {token}"})
    assert get_articles_response.ok
    assert get_articles_response.json().get("articles")[0].get("title") == "Testing APIs with Playwright from Code"
    article_to_delete = get_articles_response.json().get("articles")[0].get("slug")

    delete_article_response = api_context.delete(f"./articles/{article_to_delete}")
    assert delete_article_response.ok
