from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

class StrategyPattern(Enum):
    SINGLE_LEG = auto()
    VERTICAL_SPREAD = auto()
    STRADDLE = auto()
    STRANGLE = auto()
    COMPLEX = auto()

@dataclass(frozen=True)
class StrategyLeg:
    symbol: str
    expiry: str
    strike: float
    option_type: str  # 'Call' or 'Put'
    side: str        # 'Buy' or 'Sell'
    quantity: int

    def is_call(self):
        return self.option_type.lower() == "call"

    def is_put(self):
        return self.option_type.lower() == "put"

    def is_buy(self):
        return self.side.lower() == "buy"

    def is_sell(self):
        return self.side.lower() == "sell"

# Helper methods for strategy analysis can be added here 