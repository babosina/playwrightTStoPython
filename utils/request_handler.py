from urllib.parse import urljoin, urlencode


class RequestHandler:
    """
    Handles the construction of API request components including URL, path, query
    parameters, headers, and body. Allows chaining of methods for configuring the
    components of the request.

    Designed for usage in scenarios requiring flexible and iterative API request
    construction.

    :ivar _base_url: The base URL for the API request.
    :type _base_url: str | None
    :ivar _api_path: The API path to be appended to the base URL.
    :type _api_path: str
    :ivar _query_params: A dictionary of query parameters for the API request.
    :type _query_params: dict
    :ivar _api_headers: A dictionary of headers to be included in the API request.
    :type _api_headers: dict[str, str]
    :ivar _api_body: A dictionary representing the body of the API request.
    :type _api_body: dict
    """

    def __init__(self, api_request, base_url: str):
        self._request = api_request

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
        self._api_headers = headers
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
