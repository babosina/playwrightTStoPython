import os
import pytest

from dotenv import load_dotenv
from utils.custom_expect import expect
from utils.request_handler import RequestHandler
from utils.schema_validator import validate_schema
from copy import deepcopy
from request_data.POST_article import NEW_ARTICLE_DATA, CRUD_ARTICLE

load_dotenv()


def test_get_all_articles(api_request: RequestHandler) -> None:
    response = (api_request
                .path("./articles")
                .params({"limit": 10, "total": "zero"})
                .get_request(200))

    assert len(response.get("articles")) >= 3

    # Introducing a custom assertion
    expect(response.get("articlesCount")).should_equal(5)
    expect(response).should_match_schema("articles", "GET_articles")


# example of passing different credentials for a get_token fixture
@pytest.mark.parametrize("get_token", [
    {"email": os.getenv("EMAIL_JOHN"), "password": os.getenv("PASSWORD_JOHN")}
], indirect=True)
def test_get_all_tags(api_request: RequestHandler, get_token) -> None:
    response = api_request.path("./tags").get_request(200)
    # custom validate schema assertion
    expect(response).should_match_schema("tags", "GET_tags")
    # validate_schema("tags", "GET_tags", response_body=response)
    assert "tags" in response


def test_create_delete_article(api_request: RequestHandler, get_token) -> None:
    new_article_data = deepcopy(NEW_ARTICLE_DATA)
    new_article_data["article"]["title"] = "Import from file"
    create_article_response = (api_request
                               .path("./articles")
                               .headers({"Authorization": f"Token {get_token}"})
                               .body(new_article_data)
                               .post_request(201))
    assert create_article_response.get("article").get("title") == "Import from file"
    assert create_article_response.get("article").get("tagList") == ["Playwright"]
    expect(create_article_response).should_match_schema("articles", "POST_articles")

    get_articles_response = (api_request
                             .path("./articles")
                             .headers({"Authorization": f"Token {get_token}"})
                             .get_request(200))
    assert get_articles_response.get("articles")[0].get("title") == "Import from file"
    article_to_delete = get_articles_response.get("articles")[0].get("slug")

    (api_request
     .path(f"./articles/{article_to_delete}")
     .headers({"Authorization": f"Token {get_token}"})
     .delete_request(204))


def test_crud_article(api_request: RequestHandler, get_token) -> None:
    headers = {"Authorization": f"Token {get_token}"}

    response = (api_request
                .path("http://localhost:8000/api/articles")
                .headers(headers)
                .body(CRUD_ARTICLE)
                .post_request(201))

    assert response.get("article").get("title") == "Testing Update Delete"

    articles_response = (api_request
                         .path("./articles")
                         .headers(headers)
                         .get_request(200))
    article_to_delete = articles_response.get("articles")[0].get("slug")

    modified_title = "Testing Update Delete From Code"

    update_article_response = (api_request
                               .path(f"./articles/{article_to_delete}")
                               .headers(headers)
                               .body({"article": {"title": modified_title}})
                               .put_request(200))
    expect(update_article_response).should_match_schema("articles", "PUT_articles")

    new_slug = update_article_response.get("article").get("slug")

    (api_request
     .path(f"./articles/{new_slug}")
     .headers(headers)
     .delete_request(204))
