from abc import abstractmethod, ABC
from typing import TypeVar, Callable, Optional, List, Any, Dict, Union

HTTPParamsType = TypeVar("HTTPParamsType")
HTTPResultType = TypeVar("HTTPResultType")
WSParamsType = TypeVar("WSParamsType")
WSResultType = TypeVar("WSResultType")

HTTPParamsSchema = TypeVar("HTTPParamsSchema")
HTTPResultSchema = TypeVar("HTTPResultSchema")
WSParamsSchema = TypeVar("WSParamsSchema")
WSResultSchema = TypeVar("WSResultSchema")

AppType = TypeVar("App")

class BaseHTTPRouter(ABC):
    """
    Base HTTP router.

    In inherit class need declare http_params and http_result schemas. Input and output will be validate according
    to these schemas.
    """
    http_params_schema: HTTPParamsSchema
    http_result_schema: HTTPResultSchema

    @abstractmethod
    def _validate_schema(
            self,
            params: Union[HTTPParamsType, HTTPResultType],
    ) -> Union[HTTPParamsSchema, HTTPResultSchema]:
        """Validate parameters schema. For different framework in/out routers parameters can have diff descriptions."""
        # todo: abstract the validator

        raise NotImplementedError()

    @abstractmethod
    def get(self, http_params: HTTPParamsType) -> HTTPResultType:
        raise NotImplementedError()

    @abstractmethod
    def post(self, http_params: HTTPParamsType) -> HTTPResultType:
        raise NotImplementedError()

    @abstractmethod
    def put(self, http_params: HTTPParamsType) -> HTTPResultType:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, http_params: HTTPParamsType) -> HTTPResultType:
        raise NotImplementedError()


class BaseWSRouter(ABC):
    _send_params_schema: WSParamsSchema
    _recv_params_schema: WSResultSchema

    @abstractmethod
    def send(self, ws_params: WSParamsType) -> WSResultType:
        raise NotImplementedError()

    @abstractmethod
    def recv(self, ws_params: WSParamsType) -> WSResultType:
        raise NotImplementedError()


class BaseWebApp(ABC):
    _http_routes: List[BaseHTTPRouter] = []
    _ws_routes: List[BaseWSRouter] = []
    _app: AppType

    @abstractmethod
    def register_router(self):
        pass

    @property
    def app(self) -> AppType:
        return self._app
