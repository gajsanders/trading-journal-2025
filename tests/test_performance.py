import pytest
from src.models.performance import PerformanceMetrics
from dataclasses import asdict


def test_performance_validation():
    p = PerformanceMetrics(win_rate=0.8, total_pnl=1000, time_weighted_return=0.12, risk_adjusted_return=0.1, holding_period=10)
    assert p.validate()
    p_bad = PerformanceMetrics(win_rate=1.5)
    assert not p_bad.validate()

def test_performance_str():
    p = PerformanceMetrics(win_rate=0.7, total_pnl=500, time_weighted_return=0.08, risk_adjusted_return=0.05, holding_period=5)
    s = str(p)
    assert "PerformanceMetrics(" in s and "win_rate=0.7" in s

def test_performance_serialization():
    p = PerformanceMetrics(win_rate=0.6, total_pnl=200, time_weighted_return=0.04, risk_adjusted_return=0.03, holding_period=3)
    d = asdict(p)
    p2 = PerformanceMetrics(**d)
    assert p == p2 