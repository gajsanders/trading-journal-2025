from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from src.models.trade import Trade

@dataclass
class Position:
    entry_trades: List[Trade]
    exit_trades: List[Trade]
    status: str  # 'open' or 'closed' or 'partial'
    holding_period: Optional[float] = None  # in days
    pnl: Optional[float] = None
    time_weighted_return: Optional[float] = None

    def calculate_pnl(self):
        entries = sum(t.price * (t.quantity or 1) for t in self.entry_trades)
        exits = sum(t.price * (t.quantity or 1) for t in self.exit_trades)
        self.pnl = exits - entries
        return self.pnl

    def is_open(self):
        return self.status == 'open'

    def calculate_holding_period(self):
        if not self.entry_trades or not self.exit_trades:
            return None
        entry_time = min(t.time for t in self.entry_trades)
        exit_time = max(t.time for t in self.exit_trades)
        self.holding_period = (exit_time - entry_time).days + (exit_time - entry_time).seconds / 86400
        return self.holding_period

    def calculate_time_weighted_return(self):
        # Placeholder for actual TWR calculation
        self.time_weighted_return = self.pnl  # Simplified
        return self.time_weighted_return 