from enum import Enum
from pydantic import BaseModel
from typing import Optional, Any

Params = dict[str, str]
Headers = dict[str, str]
Cookies = dict[str, str]
Auth = dict[str, str]
Proxies = list[str]


class HTTPMethods(str, Enum):
    get: str = "get"
    post: str = "post"
    put: str = "put"
    delete: str = "delete"
    head: str = "head"


class BaseHTTPParameters(BaseModel):
    url: str
    params: Params = Params()
    headers: Headers = Headers()
    cookies: Cookies = Cookies()
    auth: Auth = Auth()
    proxies: Proxies = Proxies()
    redirection: bool = False
    certs: Optional[str] = None
    verify: bool = False
    timeout: Optional[int] = None
    trust_env: bool = True


class HTTPParameters(BaseHTTPParameters):
    content: Optional[str] = None
    data: Optional[dict] = None
    file: Optional[bytes] = None
    #json: Optional[Any] = None
