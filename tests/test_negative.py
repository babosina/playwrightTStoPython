import pytest
from utils.request_handler import RequestHandler

"""
An example of parameterized test cases for negative signup scenarios.
Doesn't work due to the API endpoint implementation on the BE.
"""


@pytest.mark.skip
@pytest.mark.parametrize(
    "username", "error_message",
    [
        {"username": "te", "error_message": "is too short (minimum is 3 characters)"},
        {"username": "tes", "error_message": ""},
        {"username": "testtesttesttesttest", "error_message": ""},
        {"username": "testtesttesttesttestt", "error_message": "is too long (maximum is 20 characters)"}
    ])
def test_negative_signup_cases(username, error_message, api_request: RequestHandler) -> None:
    response = (api_request
                .path("./users")
                .body({"user": {"email": "", "username": username, "password": "d"}})
                .post_request(422))

    if 3 < len(username) < 20:
        assert not hasattr(response, "username")
    else:
        assert response.get("username")[0] == error_message
