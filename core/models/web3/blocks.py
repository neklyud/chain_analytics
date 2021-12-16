from pydantic import BaseModel, root_validator
from typing import TypeVar


class EthTransaction(BaseModel):
    pass


Hex = TypeVar("Hex")


class EthBlock(BaseModel):
    difficulty: int
    gasLimit: int
    gasUsed: int
    hash: Hex
    logsBloom: Hex
    miner: Hex
    mixHash: Hex
    nonce: Hex
    number: int
    parentHash: Hex
    proofOfAuthorityData: Hex
    receiptsRoot: Hex
    sha3Uncles: Hex
    size: int
    stateRoot: Hex
    timestamp: int
    totalDifficulty: int
    transactions: list[Hex]
    transactionsRoot: Hex
    uncles: list

