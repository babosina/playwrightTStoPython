import pytest
import os
from dotenv import load_dotenv

load_dotenv()

from typing import Any, Generator
from playwright.sync_api import APIRequestContext, Playwright, APIResponse


@pytest.fixture(scope="module")
def get_token(api_context):
    print("GETTING USER TOKEN")
    auth_data = {
        "user": {
            "password": os.getenv("PASSWORD"),
            "email": os.getenv("EMAIL")
        }
    }
    token_response: APIResponse = api_context.post("./users/login", data=auth_data)
    token = token_response.json().get("user").get("token")

    yield token


@pytest.fixture(scope="module")
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


def test_create_article(api_context: APIRequestContext, get_token) -> None:
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
                                                            headers={"Authorization": f"Token {get_token}"},
                                                            data=new_article_data)
    assert create_article_response.ok
    assert create_article_response.json().get("article").get("title") == "Testing APIs with Playwright from Code"
    assert create_article_response.json().get("article").get("tagList") == ["Playwright"]

    get_articles_response: APIResponse = api_context.get("./articles",
                                                         headers={"Authorization": f"Token {get_token}"})
    assert get_articles_response.ok
    assert get_articles_response.json().get("articles")[0].get("title") == "Testing APIs with Playwright from Code"
    article_to_delete = get_articles_response.json().get("articles")[0].get("slug")

    delete_article_response = api_context.delete(f"./articles/{article_to_delete}",
                                                 headers={"Authorization": f"Token {get_token}"})
    assert delete_article_response.ok


def test_create_update_delete_article(api_context: APIRequestContext, get_token) -> None:
    article_data = {
        "article": {
            "title": "Testing Update Delete",
            "description": "Amazing features",
            "body": "Come use Postman for the API testing with us!",
            "tagList": []
        }
    }
    headers = {"Authorization": f"Token {get_token}"}

    response: APIResponse = api_context.post("http://localhost:8000/api/articles",
                                             headers=headers,
                                             data=article_data)
    response_json = response.json()

    assert response.ok
    assert response_json.get("article").get("title") == "Testing Update Delete"

    articles_response: APIResponse = api_context.get("./articles", headers=headers)
    articles_response_json = articles_response.json()
    article_to_delete = articles_response_json.get("articles")[0].get("slug")

    modified_title = "Testing Update Delete From Code"

    update_article_response: APIResponse = api_context.put(f"./articles/{article_to_delete}",
                                                           headers=headers,
                                                           data={
                                                               "article": {
                                                                   "title": modified_title
                                                               }
                                                           })

    update_article_response_json = update_article_response.json()
    new_slug = update_article_response_json.get("article").get("slug")

    assert update_article_response.ok

    delete_article_response: APIResponse = api_context.delete(f"./articles/{new_slug}",
                                                              headers=headers)
    assert delete_article_response.ok
