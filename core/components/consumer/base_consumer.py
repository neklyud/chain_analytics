from abc import ABC, abstractmethod
from core.models.messages.queue import QueueMessage


class BaseConsumer(ABC):
    @abstractmethod
    def _processing_message(self, *args, **kwargs) -> QueueMessage:
        raise NotImplementedError()

    @abstractmethod
    def wait_new_messages(self) -> None:
        raise NotImplementedError()
