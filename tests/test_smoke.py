def test_smoke(request):
    request.path("./articles").params({"limit": 10, "total": "zero"}).headers(
        {"Authorization": "Dummy Token"}).body({"body": "dummy body"})
