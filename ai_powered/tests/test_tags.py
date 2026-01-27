import pytest

class TestTags:
    def test_get_tags(self, api_request):
        response = (api_request
                    .path("/api/tags")
                    .get_request(200))
        
        assert "tags" in response
        assert isinstance(response["tags"], list)
        
        # Schema validation
        api_request.validate_schema(response, "ai_powered/response_schemas/tags/GET_tags_schema.json")
