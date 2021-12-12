from pydantic import BaseModel, fields
from core.enums.providers import Provider
from typing import Optional


class TransactionsLoadMessage(BaseModel):
    """
    Model of message for transactions load between start_timestamp and end_timestamp from provider.

    provider: str - source.
    start_timestamp: float.
    end_timestamp: float
    """
    provider: Provider = Provider.web3
    start_timestamp: float
    end_timestamp: float
