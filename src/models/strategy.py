from dataclasses import dataclass, field
from typing import List, Optional

class StrategyType:
    SINGLE_LEG = "SINGLE_LEG"
    VERTICAL_SPREAD = "VERTICAL_SPREAD"
    STRADDLE = "STRADDLE"
    STRANGLE = "STRANGLE"
    COMPLEX = "COMPLEX"

@dataclass
class Strategy:
    """
    Represents a detected trading strategy (single leg, spread, etc.).
    """
    type: str
    legs: List[str]
    entry_time: Optional[str] = None
    exit_time: Optional[str] = None
    pnl: Optional[float] = None

    def validate(self) -> bool:
        """Validate strategy type and legs."""
        if self.type not in (StrategyType.SINGLE_LEG, StrategyType.VERTICAL_SPREAD, StrategyType.STRADDLE, StrategyType.STRANGLE, StrategyType.COMPLEX):
            return False
        if not self.legs or not isinstance(self.legs, list):
            return False
        return True

    def __str__(self) -> str:
        return f"Strategy(type={self.type}, legs={self.legs}, entry={self.entry_time}, exit={self.exit_time}, pnl={self.pnl})" 