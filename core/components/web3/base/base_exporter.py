from abc import abstractmethod, ABC


class BaseExporter(ABC):
    @abstractmethod
    def export(self, *args: list, **kwargs: dict):
        raise NotImplementedError()