from typing import List
from src.models.position import Position
from src.models.trend_analysis import TrendAnalysis, PerformanceTrend
import numpy as np
from scipy import stats

class AdvancedAnalyzer:
    """
    Provides advanced analytics: trend detection, outlier identification, risk metrics, time-series analysis.
    """
    @staticmethod
    def detect_trend(values: List[float]) -> TrendAnalysis:
        if not values or len(values) < 2:
            return TrendAnalysis(trend=PerformanceTrend.UNKNOWN, trend_data=values)
        x = np.arange(len(values))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
        if p_value > 0.05:
            trend = PerformanceTrend.FLAT
        elif slope > 0:
            trend = PerformanceTrend.UP
        elif slope < 0:
            trend = PerformanceTrend.DOWN
        else:
            trend = PerformanceTrend.FLAT
        return TrendAnalysis(trend=trend, significance=p_value, trend_data=values)

    @staticmethod
    def identify_outliers(values: List[float], threshold: float = 3.5) -> TrendAnalysis:
        # Modified Z-Score method
        if not values:
            return TrendAnalysis(trend=PerformanceTrend.UNKNOWN, outliers=[])
        median = np.median(values)
        mad = np.median([abs(v - median) for v in values])
        if mad == 0:
            return TrendAnalysis(trend=PerformanceTrend.OUTLIER, outliers=[], trend_data=values)
        modified_z_scores = [0.6745 * (v - median) / mad for v in values]
        outliers = [v for v, mz in zip(values, modified_z_scores) if abs(mz) > threshold]
        return TrendAnalysis(trend=PerformanceTrend.OUTLIER, outliers=outliers, trend_data=values)

    @staticmethod
    def risk_metrics(values: List[float]) -> dict:
        if not values:
            return {'mean': 0.0, 'std': 0.0, 'sharpe': 0.0}
        mean = np.mean(values)
        std = np.std(values)
        sharpe = mean / std if std > 0 else 0.0
        return {'mean': mean, 'std': std, 'sharpe': sharpe}

    @staticmethod
    def time_series_analysis(values: List[float]) -> dict:
        # Example: simple moving average and volatility
        if not values:
            return {'sma': [], 'volatility': 0.0}
        sma = np.convolve(values, np.ones(5)/5, mode='valid') if len(values) >= 5 else values
        volatility = np.std(values)
        return {'sma': sma.tolist(), 'volatility': volatility} 