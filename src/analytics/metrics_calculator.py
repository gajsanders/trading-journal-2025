from typing import List, Dict, Any
from src.models.position import Position
from src.models.analytics_result import AnalyticsResult
import numpy as np

class MetricsCalculator:
    """
    Calculates performance metrics from linked positions.
    """
    @staticmethod
    def win_loss_ratio(positions: List[Position]) -> float:
        wins = sum(1 for p in positions if p.pnl is not None and p.pnl > 0)
        losses = sum(1 for p in positions if p.pnl is not None and p.pnl <= 0)
        total = wins + losses
        return wins / total if total > 0 else 0.0

    @staticmethod
    def total_pnl(positions: List[Position]) -> float:
        return sum(p.pnl for p in positions if p.pnl is not None)

    @staticmethod
    def time_weighted_return(positions: List[Position]) -> float:
        # Simplified: average of individual TWRs
        twrs = [p.time_weighted_return for p in positions if p.time_weighted_return is not None]
        return float(np.mean(twrs)) if twrs else 0.0

    @staticmethod
    def holding_periods(positions: List[Position]) -> List[float]:
        return [p.holding_period for p in positions if p.holding_period is not None]

    @staticmethod
    def risk_adjusted_return(positions: List[Position]) -> float:
        pnls = [p.pnl for p in positions if p.pnl is not None]
        if not pnls:
            return 0.0
        mean = np.mean(pnls)
        std = np.std(pnls)
        return mean / std if std > 0 else 0.0

    @staticmethod
    def group_by(positions: List[Position], key_func) -> Dict[Any, List[Position]]:
        grouped = {}
        for p in positions:
            key = key_func(p)
            grouped.setdefault(key, []).append(p)
        return grouped

    @staticmethod
    def dte_bucket(dte: float) -> str:
        if dte <= 7:
            return '0-7'
        elif dte <= 30:
            return '8-30'
        elif dte <= 60:
            return '31-60'
        else:
            return '60+'

    @staticmethod
    def calculate_all(positions: List[Position]) -> AnalyticsResult:
        result = AnalyticsResult()
        result.win_rate = MetricsCalculator.win_loss_ratio(positions)
        result.total_pnl = MetricsCalculator.total_pnl(positions)
        result.time_weighted_return = MetricsCalculator.time_weighted_return(positions)
        result.holding_periods = MetricsCalculator.holding_periods(positions)
        result.risk_adjusted_return = MetricsCalculator.risk_adjusted_return(positions)
        result.num_trades = len(positions)
        # Example grouping by DTE bucket (assuming each position has a dte attribute)
        # result.grouped_results = MetricsCalculator.group_by(positions, lambda p: MetricsCalculator.dte_bucket(getattr(p, 'dte', 0)))
        return result 