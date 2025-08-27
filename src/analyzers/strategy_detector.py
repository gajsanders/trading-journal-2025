import logging
from typing import List, Optional
from src.models.strategy_components import StrategyPattern, StrategyLeg

class StrategyDetector:
    """
    Detects common options strategies from parsed trade legs.
    """
    @staticmethod
    def detect(legs: List[StrategyLeg]) -> StrategyPattern:
        if not legs:
            logging.warning("No legs provided for strategy detection.")
            return StrategyPattern.COMPLEX
        if len(legs) == 1:
            return StrategyPattern.SINGLE_LEG
        if StrategyDetector._is_vertical_spread(legs):
            return StrategyPattern.VERTICAL_SPREAD
        if StrategyDetector._is_straddle(legs):
            return StrategyPattern.STRADDLE
        if StrategyDetector._is_strangle(legs):
            return StrategyPattern.STRANGLE
        return StrategyPattern.COMPLEX

    @staticmethod
    def _is_vertical_spread(legs: List[StrategyLeg]) -> bool:
        if len(legs) != 2:
            return False
        l1, l2 = legs
        return (
            l1.symbol == l2.symbol and
            l1.expiry == l2.expiry and
            l1.option_type == l2.option_type and
            l1.side != l2.side and
            l1.is_call() == l2.is_call() and
            l1.strike != l2.strike
        )

    @staticmethod
    def _is_straddle(legs: List[StrategyLeg]) -> bool:
        if len(legs) != 2:
            return False
        l1, l2 = legs
        return (
            l1.symbol == l2.symbol and
            l1.expiry == l2.expiry and
            l1.strike == l2.strike and
            {l1.option_type.lower(), l2.option_type.lower()} == {"call", "put"}
        )

    @staticmethod
    def _is_strangle(legs: List[StrategyLeg]) -> bool:
        if len(legs) != 2:
            return False
        l1, l2 = legs
        return (
            l1.symbol == l2.symbol and
            l1.expiry == l2.expiry and
            l1.option_type != l2.option_type and
            l1.strike != l2.strike
        ) 