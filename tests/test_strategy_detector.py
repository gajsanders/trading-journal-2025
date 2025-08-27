import pytest
from src.analyzers.strategy_detector import StrategyDetector
from src.models.strategy_components import StrategyLeg, StrategyPattern

def make_leg(symbol, expiry, strike, option_type, side, quantity):
    return StrategyLeg(symbol, expiry, strike, option_type, side, quantity)

def test_single_leg_detection():
    legs = [make_leg("AAPL", "Aug 15 30d", 150, "Call", "Buy", 1)]
    pattern = StrategyDetector.detect(legs)
    assert pattern == StrategyPattern.SINGLE_LEG

def test_vertical_spread_detection():
    legs = [
        make_leg("AAPL", "Aug 15 30d", 150, "Call", "Buy", 1),
        make_leg("AAPL", "Aug 15 30d", 155, "Call", "Sell", -1)
    ]
    pattern = StrategyDetector.detect(legs)
    assert pattern == StrategyPattern.VERTICAL_SPREAD

def test_straddle_detection():
    legs = [
        make_leg("AAPL", "Aug 15 30d", 150, "Call", "Buy", 1),
        make_leg("AAPL", "Aug 15 30d", 150, "Put", "Buy", 1)
    ]
    pattern = StrategyDetector.detect(legs)
    assert pattern == StrategyPattern.STRADDLE

def test_strangle_detection():
    legs = [
        make_leg("AAPL", "Aug 15 30d", 150, "Call", "Buy", 1),
        make_leg("AAPL", "Aug 15 30d", 155, "Put", "Buy", 1)
    ]
    pattern = StrategyDetector.detect(legs)
    assert pattern == StrategyPattern.STRANGLE

def test_complex_detection():
    # Three legs, or mismatched symbols/expiries
    legs = [
        make_leg("AAPL", "Aug 15 30d", 150, "Call", "Buy", 1),
        make_leg("AAPL", "Aug 15 30d", 155, "Call", "Sell", -1),
        make_leg("AAPL", "Aug 15 30d", 160, "Put", "Buy", 1)
    ]
    pattern = StrategyDetector.detect(legs)
    assert pattern == StrategyPattern.COMPLEX
    # Mismatched expiry
    legs2 = [
        make_leg("AAPL", "Aug 15 30d", 150, "Call", "Buy", 1),
        make_leg("AAPL", "Sep 15 30d", 155, "Call", "Sell", -1)
    ]
    pattern2 = StrategyDetector.detect(legs2)
    assert pattern2 == StrategyPattern.COMPLEX

def test_empty_legs():
    pattern = StrategyDetector.detect([])
    assert pattern == StrategyPattern.COMPLEX 