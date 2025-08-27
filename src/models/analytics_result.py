from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AnalyticsResult:
    win_rate: Optional[float] = None
    total_pnl: Optional[float] = None
    time_weighted_return: Optional[float] = None
    holding_periods: List[float] = field(default_factory=list)
    grouped_results: Dict[str, Any] = field(default_factory=dict)
    risk_adjusted_return: Optional[float] = None
    num_trades: int = 0
    aggregation: Dict[str, Any] = field(default_factory=dict)

    def aggregate(self, other: 'AnalyticsResult'):
        # Example: aggregate results from another AnalyticsResult
        self.num_trades += other.num_trades
        self.total_pnl = (self.total_pnl or 0) + (other.total_pnl or 0)
        self.holding_periods.extend(other.holding_periods)
        # Add more aggregation logic as needed 