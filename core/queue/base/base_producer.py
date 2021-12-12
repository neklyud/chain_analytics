from abc import abstractmethod, ABC
from core.models.messages.queue import QueueMessage


class BaseProducer(ABC):
    @abstractmethod
    def send(self, message: QueueMessage) -> None:
        raise NotImplementedError


class AsyncBaseProducer(ABC):
    @abstractmethod
    async def send(self, message: QueueMessage) -> None:
        raise NotImplementedError
