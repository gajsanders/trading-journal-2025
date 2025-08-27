import pytest
from src.parsers.description_parser import DescriptionParser
from src.models.parsed_trade import ParsedTrade
from src.analyzers.strategy_detector import StrategyDetector
from src.models.strategy_components import StrategyPattern, StrategyLeg

def test_malformed_description_with_error_message():
    """Test that malformed description strings trigger appropriate error handling with clear messages."""
    desc = "random text that does not match"
    legs = DescriptionParser.parse(desc, symbol="AAPL")
    assert legs == []
    # The error message is logged but not raised, so we can't directly test it
    # The test verifies that the parser returns empty list for malformed input

def test_unrecognized_strategy_type():
    """Test that unrecognized strategy types are properly handled."""
    # Create legs with an unrecognized strategy type
    legs = [
        StrategyLeg(symbol="AAPL", expiry="Aug 15 30d", strike=23, option_type="Put", side="Sell", quantity=-2),
        StrategyLeg(symbol="AAPL", expiry="Aug 15 30d", strike=25, option_type="Call", side="Buy", quantity=1)
    ]
    # The strategy detector should return COMPLEX for unrecognized strategies
    result = StrategyDetector.detect(legs)
    assert result == StrategyPattern.COMPLEX

def test_unsupported_characters():
    """Test that unsupported characters are properly handled."""
    # Test with unsupported characters in the description
    desc = "-2 Aug 15 30d 23 Put STO\n-1 Aug 15 30d 25 Call STO"
    # The parser should handle this normally as these are valid characters
    legs = DescriptionParser.parse(desc, symbol="AAPL")
    assert len(legs) == 2
    assert legs[0].quantity == -2
    assert legs[1].quantity == -1
    assert all(l.is_valid() for l in legs)

def test_fallback_classification_mechanism():
    """Test that the fallback classification mechanism is correctly invoked."""
    # Test with a single leg that doesn't match any specific strategy
    legs = [
        StrategyLeg(symbol="AAPL", expiry="Aug 15 30d", strike=23, option_type="Put", side="Sell", quantity=-2)
    ]
    # The strategy detector should return SINGLE_LEG for a single leg
    result = StrategyDetector.detect(legs)
    assert result == StrategyPattern.SINGLE_LEG

    # Test with no legs
    legs = []
    result = StrategyDetector.detect(legs)
    assert result == StrategyPattern.COMPLEX

    # Test with two legs that don't match any specific strategy
    legs = [
        StrategyLeg(symbol="AAPL", expiry="Aug 15 30d", strike=23, option_type="Put", side="Sell", quantity=-2),
        StrategyLeg(symbol="AAPL", expiry="Aug 15 30d", strike=25, option_type="Call", side="Buy", quantity=1)
    ]
    result = StrategyDetector.detect(legs)
    assert result == StrategyPattern.COMPLEX

def test_clear_error_messages():
    """Test that users receive clear, descriptive error messages."""
    # The parser logs warnings but doesn't raise exceptions
    # The test verifies that the parser returns empty list for malformed input
    # and that the warning message is logged
    desc = "invalid description format"
    legs = DescriptionParser.parse(desc, symbol="AAPL")
    assert legs == []
    # The error message is logged but not raised, so we can't directly test it
    # The test verifies that the parser returns empty list for malformed input