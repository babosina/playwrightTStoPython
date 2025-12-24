def test_smoke(api_request):
    api_request.path("./articles").params({"limit": 10, "total": "zero"}).headers(
        {"Authorization": "Dummy Token"}).body({"body": "dummy body"})
