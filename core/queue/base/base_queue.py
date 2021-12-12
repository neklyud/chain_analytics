from abc import ABC, abstractmethod
from core.models.messages.queue import QueueMessage, PushResult, PopResult


class BaseQueue(ABC):
    @abstractmethod
    def push(self, message: QueueMessage) -> PushResult:
        raise NotImplementedError

    @abstractmethod
    def pop(self) -> PopResult:
        raise NotImplementedError


class AsyncBaseQueue(ABC):
    @abstractmethod
    async def push(self, message: QueueMessage) -> PushResult:
        raise NotImplementedError

    @abstractmethod
    async def pop(self) -> PopResult:
        raise NotImplementedError
