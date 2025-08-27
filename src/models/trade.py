from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Trade:
    """
    Represents a single trade from the TastyTrade CSV.
    """
    order_id: str
    symbol: str
    expiry: str
    strike: float
    option_type: str
    side: str
    quantity: int
    price: float
    time: str
    # Add more fields as needed

    def validate(self) -> bool:
        """Validate required fields and types."""
        if not self.order_id or not self.symbol or not self.expiry:
            return False
        if self.option_type not in ("Call", "Put"):
            return False
        if self.side not in ("BTO", "STO", "BTC", "STC"):
            return False
        if not isinstance(self.quantity, int) or self.quantity == 0:
            return False
        return True

    def __str__(self) -> str:
        return f"Trade({self.order_id}, {self.symbol}, {self.expiry}, {self.strike}, {self.option_type}, {self.side}, {self.quantity}, {self.price}, {self.time})" 