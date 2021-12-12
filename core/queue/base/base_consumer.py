from abc import abstractmethod, ABC
from core.models.messages.queue import QueueMessage
from core.queue.base.base_queue import BaseQueue


class BaseConsumer(ABC):
    @abstractmethod
    def wait(self) -> QueueMessage:
        raise NotImplementedError


class AsyncBaseConsumer(ABC):
    @abstractmethod
    async def wait(self) -> QueueMessage:
        raise NotImplementedError

