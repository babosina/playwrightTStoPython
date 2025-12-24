def test_smoke(api_request):
    response = (api_request
                .path("./articles")
                .params({"limit": 10, "total": "zero"})
                .get_request(200))

    assert len(response.get("articles")) >= 3
    assert response.get("articlesCount") == 5


def test_get_all_tags(api_request):
    response = api_request.path("./tags").get_request(200)
    assert "tags" in response
