from abc import ABC, abstractmethod
from typing import TypeVar, Generic

ComponentType = TypeVar("ComponentType")


class BaseComponentFactory(ABC, Generic[ComponentType]):
    @abstractmethod
    def create(self, component_name: str) -> ComponentType:
        raise NotImplementedError()

