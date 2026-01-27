import pytest

class TestArticles:
    def test_list_articles(self, api_request):
        params = {"limit": 10, "offset": 0}
        response = (api_request
                    .path("/api/articles")
                    .params(params)
                    .get_request(200))
        
        assert "articles" in response
        assert "articlesCount" in response
        api_request.validate_schema(response, "ai_powered/response_schemas/articles/GET_articles_schema.json")

    def test_create_article(self, api_request, auth_headers, article_generator):
        article_data = article_generator.generate_article_data()
        
        response = (api_request
                    .path("/api/articles")
                    .headers(auth_headers)
                    .body(article_data)
                    .post_request(201)) # conduit usually returns 201 for POST
        
        assert "article" in response
        assert response["article"]["title"] == article_data["article"]["title"]
        api_request.validate_schema(response, "ai_powered/response_schemas/articles/POST_articles_schema.json")
        
        # Cleanup
        slug = response["article"]["slug"]
        api_request.path(f"/api/articles/{slug}").headers(auth_headers).delete_request(204)

    def test_update_article(self, api_request, auth_headers, article_generator):
        # First create an article
        article_data = article_generator.generate_article_data()
        created_article = (api_request
                           .path("/api/articles")
                           .headers(auth_headers)
                           .body(article_data)
                           .post_request(201))
        
        slug = created_article["article"]["slug"]
        
        # Update it
        update_data = {
            "article": {
                "title": f"Updated {article_data['article']['title']}"
            }
        }
        
        updated_response = (api_request
                            .path(f"/api/articles/{slug}")
                            .headers(auth_headers)
                            .body(update_data)
                            .put_request(200))
        
        assert updated_response["article"]["title"] == update_data["article"]["title"]
        api_request.validate_schema(updated_response, "ai_powered/response_schemas/articles/PUT_articles_schema.json")
        
        # Cleanup
        api_request.path(f"/api/articles/{slug}").headers(auth_headers).delete_request(204)

    def test_delete_article(self, api_request, auth_headers, article_generator):
        article_data = article_generator.generate_article_data()
        created_article = (api_request
                           .path("/api/articles")
                           .headers(auth_headers)
                           .body(article_data)
                           .post_request(201))
        
        slug = created_article["article"]["slug"]
        
        # Delete it
        api_request.path(f"/api/articles/{slug}").headers(auth_headers).delete_request(204)
        
        # Verify it's gone
        api_request.path(f"/api/articles/{slug}").get_request(404)

    def test_create_article_unauthorized(self, api_request, article_generator):
        article_data = article_generator.generate_article_data()
        
        api_request.path("/api/articles").body(article_data).post_request(401)
