from typing import List
import json
from pydantic import BaseModel, validator
import os
from enum import Enum


class ComponentTypeEnum(str, Enum):
    queue: str = "queue"
    web: str = "web"
    producer: str = "producer"
    consumer: str = "consumer"
    db: str = "db"
    storage: str = "storage"


class Component(BaseModel):
    component_type: ComponentTypeEnum
    component_name: str


class ServiceConfig(BaseModel):
    service_name: str
    components: List[Component]

    @validator("service_name")
    def check_service_name(cls, v) -> str:
        assert v
        return v


def load_config(path_to_config: str) -> ServiceConfig:
    if not os.path.exists(path_to_config):
        raise Exception("Invalid path to config.")
    with open(path_to_config, 'rb') as service_json:
        cfg_json = json.loads(service_json.read())
    return ServiceConfig(**cfg_json)
