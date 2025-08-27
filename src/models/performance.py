from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class PerformanceMetrics:
    """
    Holds performance metrics for a set of trades or a strategy.
    """
    win_rate: Optional[float] = None
    total_pnl: Optional[float] = None
    time_weighted_return: Optional[float] = None
    risk_adjusted_return: Optional[float] = None
    holding_period: Optional[float] = None

    def validate(self) -> bool:
        """Validate that metrics are within expected ranges."""
        if self.win_rate is not None and not (0 <= self.win_rate <= 1):
            return False
        # Add more checks as needed
        return True

    def __str__(self) -> str:
        return f"PerformanceMetrics(win_rate={self.win_rate}, pnl={self.total_pnl}, twr={self.time_weighted_return}, risk_adj={self.risk_adjusted_return}, holding={self.holding_period})"

    @staticmethod
    def calculate_win_rate(trade_results: List[bool]) -> float:
        """Calculate win rate from a list of trade results (True=win, False=loss)."""
        if not trade_results:
            return 0.0
        return sum(trade_results) / len(trade_results)

    @staticmethod
    def calculate_total_pnl(pnls: List[float]) -> float:
        """Calculate total PnL from a list of trade PnLs."""
        return sum(pnls) if pnls else 0.0

    def __repr__(self):
        return self.__str__() 