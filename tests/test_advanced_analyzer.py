import pytest
from src.analytics.advanced_analyzer import AdvancedAnalyzer
from src.models.trend_analysis import PerformanceTrend

def test_detect_trend_up():
    values = [1, 2, 3, 4, 5]
    result = AdvancedAnalyzer.detect_trend(values)
    assert result.trend == PerformanceTrend.UP
    assert result.significance is not None

def test_detect_trend_down():
    values = [5, 4, 3, 2, 1]
    result = AdvancedAnalyzer.detect_trend(values)
    assert result.trend == PerformanceTrend.DOWN

def test_detect_trend_flat():
    values = [2, 2, 2, 2, 2]
    result = AdvancedAnalyzer.detect_trend(values)
    assert result.trend == PerformanceTrend.FLAT

def test_detect_trend_unknown():
    values = [1]
    result = AdvancedAnalyzer.detect_trend(values)
    assert result.trend == PerformanceTrend.UNKNOWN

def test_identify_outliers():
    values = [1, 2, 3, 10, 100]
    result = AdvancedAnalyzer.identify_outliers(values, threshold=2)
    assert PerformanceTrend.OUTLIER == result.trend
    assert 100 in result.outliers

def test_identify_outliers_none():
    values = [1, 2, 3, 4]
    result = AdvancedAnalyzer.identify_outliers(values, threshold=2)
    assert result.outliers == []

def test_risk_metrics():
    values = [10, 20, 30]
    metrics = AdvancedAnalyzer.risk_metrics(values)
    assert pytest.approx(metrics['mean']) == 20
    assert pytest.approx(metrics['std'], rel=1e-3) == 8.1649658
    assert pytest.approx(metrics['sharpe'], rel=1e-3) == 2.4494897

def test_time_series_analysis():
    values = [1, 2, 3, 4, 5, 6, 7]
    result = AdvancedAnalyzer.time_series_analysis(values)
    assert 'sma' in result
    assert 'volatility' in result
    assert isinstance(result['sma'], list)
    assert isinstance(result['volatility'], float)

def test_time_series_analysis_empty():
    result = AdvancedAnalyzer.time_series_analysis([])
    assert result['sma'] == []
    assert result['volatility'] == 0.0 