import pytest
from src.analytics.metrics_calculator import MetricsCalculator
from src.models.position import Position

class DummyPosition(Position):
    def __init__(self, pnl=None, time_weighted_return=None, holding_period=None, dte=None):
        super().__init__(entry_trades=[], exit_trades=[], status='closed')
        self.pnl = pnl
        self.time_weighted_return = time_weighted_return
        self.holding_period = holding_period
        self.dte = dte

def test_win_loss_ratio():
    positions = [DummyPosition(pnl=10), DummyPosition(pnl=-5), DummyPosition(pnl=0)]
    assert MetricsCalculator.win_loss_ratio(positions) == pytest.approx(1/3)
    assert MetricsCalculator.win_loss_ratio([]) == 0.0

def test_total_pnl():
    positions = [DummyPosition(pnl=10), DummyPosition(pnl=-5), DummyPosition(pnl=2)]
    assert MetricsCalculator.total_pnl(positions) == 7
    assert MetricsCalculator.total_pnl([]) == 0

def test_time_weighted_return():
    positions = [DummyPosition(time_weighted_return=0.1), DummyPosition(time_weighted_return=0.2)]
    assert MetricsCalculator.time_weighted_return(positions) == pytest.approx(0.15)
    assert MetricsCalculator.time_weighted_return([]) == 0.0

def test_holding_periods():
    positions = [DummyPosition(holding_period=5), DummyPosition(holding_period=10)]
    assert MetricsCalculator.holding_periods(positions) == [5, 10]
    assert MetricsCalculator.holding_periods([]) == []

def test_risk_adjusted_return():
    positions = [DummyPosition(pnl=10), DummyPosition(pnl=20), DummyPosition(pnl=30)]
    # mean = 20, std = 8.1649658, mean/std = 2.4494897
    assert MetricsCalculator.risk_adjusted_return(positions) == pytest.approx(2.4494897, rel=1e-3)
    assert MetricsCalculator.risk_adjusted_return([]) == 0.0

def test_group_by():
    positions = [DummyPosition(pnl=1, dte=5), DummyPosition(pnl=2, dte=10), DummyPosition(pnl=3, dte=5)]
    grouped = MetricsCalculator.group_by(positions, lambda p: p.dte)
    assert set(grouped.keys()) == {5, 10}
    assert len(grouped[5]) == 2
    assert len(grouped[10]) == 1

def test_dte_bucket():
    assert MetricsCalculator.dte_bucket(3) == '0-7'
    assert MetricsCalculator.dte_bucket(15) == '8-30'
    assert MetricsCalculator.dte_bucket(45) == '31-60'
    assert MetricsCalculator.dte_bucket(90) == '60+'

def test_calculate_all():
    positions = [DummyPosition(pnl=10, time_weighted_return=0.1, holding_period=5), DummyPosition(pnl=-5, time_weighted_return=0.2, holding_period=10)]
    result = MetricsCalculator.calculate_all(positions)
    assert result.win_rate == pytest.approx(0.5)
    assert result.total_pnl == 5
    assert result.time_weighted_return == pytest.approx(0.15)
    assert result.holding_periods == [5, 10]
    assert result.num_trades == 2 