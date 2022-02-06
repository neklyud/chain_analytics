from abc import abstractmethod, ABC


class BaseSource(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError()


class BaseTarget(ABC):
    @abstractmethod
    def push_data(self):
        raise NotImplementedError()


class BaseAsyncSource(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError()


class BaseAsyncTarget(ABC):
    @abstractmethod
    async def push_data(self, *args, **kwargs):
        raise NotImplementedError()


class BaseLoader(ABC):
    def __init__(self, source: BaseSource, target: BaseTarget):
        self.source: BaseSource = source
        self.target: BaseTarget = target

    @abstractmethod
    def load(self):
        raise NotImplementedError()


class AsyncBaseLoader(ABC):
    ...
