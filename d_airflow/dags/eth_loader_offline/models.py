from datetime import datetime
from dataclasses import dataclass


@dataclass
class BlocksNumbersByPeriodParams(object):

    start_timestamp: datetime
    end_timestamp: datetime
