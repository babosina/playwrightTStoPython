import pytest
import os

class TestAuth:
    def test_login_success(self, api_request):
        email = os.getenv("EMAIL", "")
        password = os.getenv("PASSWORD", "")
        
        auth_data = {
            "user": {
                "email": email,
                "password": password
            }
        }
        
        response = (api_request
                    .path("/api/users/login")
                    .body(auth_data)
                    .post_request(200))
        
        assert "user" in response
        assert "token" in response["user"]
        assert response["user"]["email"] == email

    def test_login_invalid_credentials(self, api_request):
        auth_data = {
            "user": {
                "email": "wrong@example.com",
                "password": "wrongpassword"
            }
        }
        
        # Based on typical Conduit API, it returns 403 or 401 for invalid credentials
        # Let's try 401/403 and catch the error if it's different
        try:
            api_request.path("/api/users/login").body(auth_data).post_request(403)
        except AssertionError:
             api_request.path("/api/users/login").body(auth_data).post_request(401)

    def test_login_missing_fields(self, api_request):
        auth_data = {
            "user": {
                "email": ""
            }
        }
        
        # 422 Unprocessable Entity is expected for missing fields
        api_request.path("/api/users/login").body(auth_data).post_request(422)
