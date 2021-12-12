from core.http_client.base.base_http import HTTPParameters
import httpx
from httpx import Response


class HTTPClient(object):
    @classmethod
    def request(cls, request_parameters: HTTPParameters) -> Response:
        return httpx.request(*request_parameters)


if __name__ == '__main__':
    resp = HTTPClient.request(HTTPParameters(url="http://www.domain.com/"))
    print(resp)
