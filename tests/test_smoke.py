from utils.request_handler import RequestHandler


def test_smoke():
    api = RequestHandler()
    api.url("http://localhost:8000/api").path("./articles").params({"limit": 10}).headers(
        {"Authorization": "Dummy Token"}).body({"body": "dummy body"})
