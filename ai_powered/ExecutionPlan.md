# API Testing Execution Plan

This document outlines the strategy for automated API testing of the RESTful API located at `http://localhost:8000/api`.

## 1. Testing Stack
- **Language**: Python
- **Testing Framework**: `pytest`
- **HTTP Client**: `Playwright` (via `APIRequestContext`) or `requests`
- **Validation**: `jsonschema` for response schema validation
- **Reporting**: Allure (based on existing project structure)

## 2. Test Environment
- **Base URL**: `http://localhost:8000/api`
- **Authentication**: JWT token obtained via `POST /users/login`

## 3. Test Scenarios

### 3.1 Authentication
- **POST /users/login**
    - [Positive] Valid credentials returns 200 OK and a token.
    - [Negative] Invalid credentials returns 403/401 Forbidden/Unauthorized.
    - [Negative] Missing fields (email/password) returns 422 Unprocessable Entity.

### 3.2 Tags
- **GET /tags**
    - [Positive] Retrieve all tags, validate schema and non-empty list.

### 3.3 Articles (CRUD Operations)
- **GET /articles**
    - [Positive] List articles with default pagination.
    - [Positive] List articles with `limit` and `offset` parameters.
- **POST /articles**
    - [Positive] Create a new article with valid data and auth token.
    - [Negative] Create article without auth token (401).
    - [Negative] Create article with missing required fields (422).
- **PUT /articles/{slug}**
    - [Positive] Update an existing article's title/body.
    - [Negative] Update article belonging to another user (403).
- **DELETE /articles/{slug}**
    - [Positive] Delete an article.
    - [Negative] Delete non-existent article (404).

## 4. Response Validation
All responses will be validated against JSON schemas located in `response_schemas/`:
- `GET_tags_schema.json`
- `GET_articles_schema.json`
- `POST_articles_schema.json`
- `PUT_articles_schema.json`

## 5. Proposed Project Structure
```text
tests/
├── conftest.py          # Fixtures for api_request, auth token, etc.
├── test_auth.py         # Login tests
├── test_tags.py         # Tag retrieval tests
└── test_articles.py     # Article CRUD tests
utils/
├── request_handler.py   # Wrapper for API calls (Playwright based)
├── article_generator.py # Data factory for dynamic article creation
└── custom_expect.py     # Custom assertions if needed
response_schemas/        # JSON schemas for validation
```

## 6. Execution Flow
1. **Setup**: Initialize `APIRequestContext` and obtain Auth Token via `conftest.py` fixtures.
2. **Execution**: Run `pytest` command.
3. **Validation**: 
    - Verify Status Codes.
    - Validate JSON Schema.
    - Verify business logic (e.g., article content matches request).
4. **Teardown**: Clean up created articles if necessary.
