from abc import abstractmethod, ABC


class BaseSource(ABC):
    @abstractmethod
    def get_data(self, *args, **kwargs):
        raise NotImplementedError()


class BaseReceiver(ABC):
    @abstractmethod
    def push_data(self):
        raise NotImplementedError()


class BaseLoader(ABC):
    def __init__(self, source: BaseSource, receiver: BaseReceiver):
        self.source: BaseSource = source
        self.target: BaseReceiver = receiver

    @abstractmethod
    def run(self):
        raise NotImplementedError()

