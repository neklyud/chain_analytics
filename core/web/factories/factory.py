from abc import abstractmethod, ABC
from core.web.base.base_web import BaseWebApp


class BaseWebAppFactory(ABC):
    @abstractmethod
    def create(self) -> BaseWebApp:
        raise NotImplementedError()

