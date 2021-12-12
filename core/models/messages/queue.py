from pydantic import BaseModel, Json
from core.enums.queue import PushStatus


class QueueMessage(BaseModel):
    id: int
    data: dict


class PushResult(BaseModel):
    status: PushStatus
    description: str


class PopResult(BaseModel):
    data: dict
