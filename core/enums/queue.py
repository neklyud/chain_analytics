from enum import Enum


class PushStatus(str, Enum):
    success: str = "success"
    failed: str = "failed"
