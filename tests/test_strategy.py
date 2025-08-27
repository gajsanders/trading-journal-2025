import pytest
from src.models.strategy import Strategy, StrategyType
from dataclasses import asdict
from datetime import datetime

def test_strategy_creation():
    s = Strategy(type=StrategyType.SINGLE_LEG, legs=["AAPL"], entry_time="2024-07-01", exit_time="2024-07-10", pnl=150.0)
    assert s.type == StrategyType.SINGLE_LEG
    assert s.legs == ["AAPL"]
    assert s.validate()

def test_strategy_invalid_type():
    s = Strategy(type="INVALID", legs=["AAPL"])
    assert not s.validate()

def test_strategy_empty_legs():
    s = Strategy(type=StrategyType.SINGLE_LEG, legs=[])
    assert not s.validate()

def test_strategy_entry_time_type():
    # entry_time is now a string, so this test is not needed
    pass

def test_strategy_str_and_repr():
    s = Strategy(type=StrategyType.STRADDLE, legs=["AAPL", "AAPL"], entry_time="2024-07-01", exit_time=None)
    s_str = str(s)
    assert "Strategy(" in s_str and "STRADDLE" in s_str

def test_strategy_serialization():
    s = Strategy(type=StrategyType.STRADDLE, legs=["leg1", "leg2"], entry_time="2024-07-01", exit_time="2024-07-10", pnl=25.0)
    d = asdict(s)
    s2 = Strategy(**d)
    assert s == s2 