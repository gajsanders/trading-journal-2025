import pytest
from src.parsers.description_parser import DescriptionParser
from src.models.parsed_trade import ParsedTrade

def test_single_leg_parsing():
    desc = "-2 Aug 15 30d 23 Put STO"
    legs = DescriptionParser.parse(desc, symbol="AAPL")
    assert len(legs) == 1
    leg = legs[0]
    assert leg.symbol == "AAPL"
    assert leg.expiry == "Aug 15 30d"
    assert leg.strike == 23
    assert leg.option_type == "Put"
    assert leg.side == "Sell"
    assert leg.quantity == -2
    assert leg.is_valid()

def test_multi_leg_parsing():
    desc = "-1 Jul 31 15d 5400 Put STO\n1 Jul 31 15d 5325 Put BTO"
    legs = DescriptionParser.parse(desc, symbol="/MESU5")
    assert len(legs) == 2
    assert legs[0].quantity == -1
    assert legs[1].quantity == 1
    assert legs[0].option_type == "Put"
    assert legs[1].option_type == "Put"
    assert legs[0].side == "Sell"
    assert legs[1].side == "Buy"
    assert legs[0].expiry == "Jul 31 15d"
    assert legs[1].expiry == "Jul 31 15d"
    assert legs[0].strike == 5400
    assert legs[1].strike == 5325
    assert all(l.is_valid() for l in legs)

def test_futures_option_parsing():
    desc = "-1 Aug 1 16d 5975 Put STO"
    legs = DescriptionParser.parse(desc, symbol="/MESU5")
    assert len(legs) == 1
    leg = legs[0]
    assert leg.symbol == "/MESU5"
    assert leg.strike == 5975
    assert leg.option_type == "Put"
    assert leg.side == "Sell"
    assert leg.quantity == -1
    assert leg.is_valid()

def test_malformed_description():
    desc = "random text that does not match"
    legs = DescriptionParser.parse(desc, symbol="AAPL")
    assert legs == []

def test_empty_description():
    legs = DescriptionParser.parse("", symbol="AAPL")
    assert legs == [] 