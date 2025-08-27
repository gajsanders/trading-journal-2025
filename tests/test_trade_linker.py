import pytest
from src.analyzers.trade_linker import TradeLinker
from src.models.trade import Trade
from datetime import datetime

def make_trade(order_id, symbol, price, time, quantity, side, expiry="2024-07-19", strike=100.0, option_type="Call"):
    return Trade(
        order_id=order_id,
        symbol=symbol,
        expiry=expiry,
        strike=strike,
        option_type=option_type,
        side=side,
        quantity=quantity,
        price=price,
        time=str(time)
    )

def test_sto_btc_linking():
    t1 = make_trade("1", "AAPL", 1.0, datetime(2023,1,1,10), 1, "STO")
    t2 = make_trade("1", "AAPL", -1.0, datetime(2023,1,2,10), -1, "BTC")
    linker = TradeLinker([t1, t2])
    positions = linker.link_trades()
    assert len(positions) == 1
    pos = positions[0]
    assert pos.entry_trades[0] == t1
    assert pos.exit_trades[0] == t2

def test_bto_stc_linking():
    t1 = make_trade("3", "AAPL", 2.0, datetime(2023,1,1,10), 1, "BTO")
    t2 = make_trade("3", "AAPL", -2.0, datetime(2023,1,2,10), -1, "STC")
    linker = TradeLinker([t1, t2])
    positions = linker.link_trades()
    assert len(positions) == 1
    pos = positions[0]
    assert pos.entry_trades[0] == t1
    assert pos.exit_trades[0] == t2

def test_partial_closure():
    t1 = make_trade("5", "AAPL", 1.0, datetime(2023,1,1,10), 2, "STO")
    t2 = make_trade("5", "AAPL", -1.0, datetime(2023,1,2,10), -1, "BTC")
    t3 = make_trade("5", "AAPL", -1.0, datetime(2023,1,3,10), -1, "BTC")
    linker = TradeLinker([t1, t2, t3])
    positions = linker.link_trades()
    assert len(positions) == 1
    pos = positions[0]
    assert len(pos.entry_trades) == 1
    assert len(pos.exit_trades) == 2

def test_edge_case_missing_exit():
    t1 = make_trade("8", "AAPL", 1.0, datetime(2023,1,1,10), 1, "STO")
    linker = TradeLinker([t1])
    positions = linker.link_trades()
    assert len(positions) == 1
    pos = positions[0]
    assert len(pos.exit_trades) == 0

def test_edge_case_missing_entry():
    t1 = make_trade("9", "AAPL", 1.0, datetime(2023,1,1,10), 1, "BTC")
    linker = TradeLinker([t1])
    positions = linker.link_trades()
    assert len(positions) == 1
    pos = positions[0]
    assert len(pos.entry_trades) == 0 