from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass(frozen=True)
class ParsedTrade:
    """
    Represents a parsed trade leg from a TastyTrade description.
    """
    symbol: str
    expiry: str
    strike: float
    option_type: str  # 'Call' or 'Put'
    side: str        # 'Buy' or 'Sell'
    quantity: int
    raw: str = field(default="")

    def is_valid(self) -> bool:
        return all([
            self.symbol,
            self.expiry,
            self.strike is not None,
            self.option_type in ("Call", "Put"),
            self.side in ("Buy", "Sell"),
            self.quantity != 0
        ])

    def identify_characteristics(self):
        # Stub for future characteristic identification
        pass 