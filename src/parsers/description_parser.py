import re
import logging
from typing import List
from src.models.parsed_trade import ParsedTrade

class DescriptionParser:
    """
    Parses TastyTrade description fields into structured ParsedTrade objects.
    """
    # Example: -2 Aug 15 30d 23 Put STO
    SINGLE_LEG_PATTERN = re.compile(r"(?P<qty>[-+]?\d+)\s+(?P<expiry>[A-Za-z0-9 ]+)\s+(?P<strike>[\d.]+)\s+(?P<type>Call|Put)\s+(?P<side>STO|BTC|BTO|STC)", re.IGNORECASE)
    # Multi-leg: one per line

    @classmethod
    def parse(cls, description: str, symbol: str = "") -> List[ParsedTrade]:
        if not description:
            logging.warning("Empty description string.")
            return []
        legs = []
        for line in description.splitlines():
            match = cls.SINGLE_LEG_PATTERN.search(line.strip())
            if match:
                qty = int(match.group("qty"))
                expiry = match.group("expiry").strip()
                strike = float(match.group("strike"))
                option_type = match.group("type").capitalize()
                side_code = match.group("side").upper()
                side = "Sell" if side_code in ("STO", "STC") else "Buy"
                legs.append(ParsedTrade(
                    symbol=symbol,
                    expiry=expiry,
                    strike=strike,
                    option_type=option_type,
                    side=side,
                    quantity=qty,
                    raw=line.strip()
                ))
            else:
                logging.warning(f"Could not parse line: {line}")
        return legs 