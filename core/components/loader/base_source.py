from abc import ABC, abstractmethod
from core.models.web3.blocks import EthBlock, Hex


class AsyncBaseWeb3(ABC):
    @abstractmethod
    async def get_block(self, block_number: int) -> EthBlock:
        raise NotImplementedError()

    @abstractmethod
    async def get_transaction(self, trx_hash: Hex):
        raise NotImplementedError()
    