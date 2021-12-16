from abc import ABC, abstractmethod
from core.models.messages.queue import QueueMessage


class BaseSyncProducer:
    @abstractmethod
    def send(self, message: QueueMessage):
        raise NotImplementedError()
