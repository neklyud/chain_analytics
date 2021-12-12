from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type
from core.models.messages.queue import QueueMessage
from core.factory.base.base_component import BaseComponentFactory

QueueType = TypeVar("QueueType")


class BaseQueue(ABC, Generic[QueueType]):
    _queue: QueueType

    @property
    def queue(self) -> QueueType:
        return self._queue

    @abstractmethod
    def push(self, msg: QueueMessage) -> None:
        raise NotImplementedError()

    @abstractmethod
    def pop(self) -> QueueMessage:
        raise NotImplementedError()

    @abstractmethod
    def wait_new_messages(self) -> QueueMessage:
        raise NotImplementedError()


class BaseAsyncQueue(ABC, Generic[QueueType]):
    _queue: QueueType

    @property
    async def queue(self) -> QueueType:
        return self._queue

    @abstractmethod
    async def push(self, msg: QueueMessage) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def pop(self) -> QueueMessage:
        raise NotImplementedError()

    @abstractmethod
    async def wait_new_messages(self) -> QueueMessage:
        raise NotImplementedError()


class QueueFactory(BaseComponentFactory[BaseQueue]):
    _queues: dict[str, Type[BaseQueue]]

    def create(self, component_name: str) -> BaseQueue:
        if component_name in self._queues.keys():
            return self._queues[component_name]()
        raise KeyError(f"Queue {component_name} not exists.")
