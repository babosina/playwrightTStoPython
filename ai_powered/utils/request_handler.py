import json
import os
from urllib.parse import urljoin, urlencode
from playwright.sync_api import APIRequestContext
from jsonschema import validate, ValidationError

# Importing from the root utils as they are already implemented and reusable
from utils.apilogger import APILogger

class RequestHandler:
    def __init__(self, api_request: APIRequestContext, base_url: str, logger: APILogger):
        self._request: APIRequestContext = api_request
        self._logger: APILogger = logger

        # request state
        self._base_url: str | None = None
        self._default_base_url: str = base_url
        self._api_path: str = ""
        self._query_params: dict = dict()
        self._api_headers: dict[str, str] = dict()
        self._api_body: dict = dict()

    def url(self, url: str):
        self._base_url = url
        return self

    def path(self, path: str):
        self._api_path = path
        return self

    def params(self, params: dict):
        self._query_params = params
        return self

    def headers(self, headers: dict):
        self._api_headers.update(headers)
        return self

    def body(self, body: dict):
        self._api_body = body
        return self

    def _get_url(self):
        base_url = self._base_url or self._default_base_url
        url = urljoin(base_url, self._api_path)

        if self._query_params:
            query_string = urlencode(self._query_params)
            url = f"{url}?{query_string}"

        return url

    def get_request(self, status_code: int):
        url = self._get_url()
        self._logger.log_request("GET", url, self._api_headers)
        response = self._request.get(url, headers=self._api_headers)
        resp_json = response.json() if response.status != 204 else {}
        self._cleanup_fields()
        self._logger.log_response(response.status, resp_json)
        self._status_code_validator(response.status, status_code)
        return resp_json

    def post_request(self, status_code: int):
        url = self._get_url()
        self._logger.log_request("POST", url, self._api_headers, self._api_body)
        response = self._request.post(url,
                                      headers=self._api_headers,
                                      data=self._api_body)
        resp_json = response.json() if response.status != 204 else {}
        self._cleanup_fields()
        self._logger.log_response(response.status, resp_json)
        self._status_code_validator(response.status, status_code)
        return resp_json

    def put_request(self, status_code: int):
        url = self._get_url()
        self._logger.log_request("PUT", url, self._api_headers, self._api_body)
        response = self._request.put(url,
                                     headers=self._api_headers,
                                     data=self._api_body)
        resp_json = response.json() if response.status != 204 else {}
        self._cleanup_fields()
        self._logger.log_response(response.status, resp_json)
        self._status_code_validator(response.status, status_code)
        return resp_json

    def delete_request(self, status_code: int):
        url = self._get_url()
        self._logger.log_request("DELETE", url, self._api_headers)
        response = self._request.delete(url, headers=self._api_headers)
        self._cleanup_fields()
        self._logger.log_response(response.status)
        self._status_code_validator(response.status, status_code)
        return response.status

    def validate_schema(self, response_data: dict, schema_path: str):
        # schema_path should be relative to the project root or absolute
        abs_schema_path = os.path.abspath(schema_path)
        with open(abs_schema_path, 'r') as f:
            schema = json.load(f)
        try:
            validate(instance=response_data, schema=schema)
        except ValidationError as e:
            raise ValidationError(f"Schema validation failed: {e.message}")

    def _status_code_validator(self, actual_status: int, expected_status: int):
        if actual_status != expected_status:
            logs = self._logger.get_recent_logs()
            error = f"Expected status code {expected_status} but got {actual_status}\n\nRecent API activity: \n{logs}"
            raise AssertionError(error)

    def _cleanup_fields(self):
        self._api_body = dict()
        self._api_headers = dict()
        self._base_url = None
        self._api_path = ""
        self._query_params = dict()
