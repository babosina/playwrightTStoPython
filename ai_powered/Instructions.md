You act as a software test engineer. Your task is to create a plan for the automated API testing.
Your stack is Python, using libraries such as pytest, requests, and jsonschema for testing.
You can also use Playwright to get built-in fixtures if you want.

The application under test is a RESTful API. 

The API is available at http://localhost:8000/api

Examples of the API endpoints are provided below.

- POST /users/login # get auth token
- GET /tags # get all tags
- GET /articles?limit=10&offset=0 # get articles
- POST /articles # create article
- PUT /articles/{slug} # update article
- DELETE /articles/{slug} # delete article

Example body for the auth request:
```json
{
    "user": {
        "email": "some_email",
        "password": "some_password"
    }
}
```

Example body for a new article request:
```json
{
    "article": {
        "title": "Testing APIs with Postman from Postman",
        "description": "Amazing features",
        "body": "Come use Postman for the API testing with us!",
        "tagList": [
            "Playwright"
        ]
    }
}
```

You can use response schemas to validate the responses. Response schemas can be found in the `playwrightTStoPython/response_schemas` directory.

In the current folder create a new file named ExecutionPlan.md and write your plan there.

