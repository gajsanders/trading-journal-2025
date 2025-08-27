import pytest
from src.models.trade import Trade
from dataclasses import asdict

def test_trade_validation():
    t = Trade(order_id="1", symbol="AAPL", expiry="2024-07-19", strike=150.0, option_type="Call", side="BTO", quantity=1, price=2.5, time="2024-07-01 09:30")
    assert t.validate()
    t_bad = Trade(order_id="", symbol="AAPL", expiry="2024-07-19", strike=150.0, option_type="Call", side="BTO", quantity=1, price=2.5, time="2024-07-01 09:30")
    assert not t_bad.validate()
    t_bad2 = Trade(order_id="1", symbol="AAPL", expiry="2024-07-19", strike=150.0, option_type="Foo", side="BTO", quantity=1, price=2.5, time="2024-07-01 09:30")
    assert not t_bad2.validate()
    t_bad3 = Trade(order_id="1", symbol="AAPL", expiry="2024-07-19", strike=150.0, option_type="Call", side="BTO", quantity=0, price=2.5, time="2024-07-01 09:30")
    assert not t_bad3.validate()

def test_trade_str():
    t = Trade(order_id="1", symbol="AAPL", expiry="2024-07-19", strike=150.0, option_type="Call", side="BTO", quantity=1, price=2.5, time="2024-07-01 09:30")
    s = str(t)
    assert "Trade(" in s and "AAPL" in s

def test_trade_serialization():
    t = Trade(order_id="1", symbol="AAPL", expiry="2024-07-19", strike=150.0, option_type="Call", side="BTO", quantity=1, price=2.5, time="2024-07-01 09:30")
    d = asdict(t)
    t2 = Trade(**d)
    assert t == t2 