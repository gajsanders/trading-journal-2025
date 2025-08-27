import os
import base64
from src.visualizations.chart_generator import ChartGenerator

def test_cumulative_pnl_chart(tmp_path):
    pnls = [10, -5, 20, -10]
    md = ChartGenerator.cumulative_pnl_chart(pnls)
    assert md.startswith('![')
    # Test file saving
    path = tmp_path / "cum_pnl.png"
    ChartGenerator.cumulative_pnl_chart(pnls, save_path=str(path))
    assert os.path.exists(path)

def test_win_loss_ratio_chart():
    win_loss = [True, False, True, True, False]
    md = ChartGenerator.win_loss_ratio_chart(win_loss)
    assert md.startswith('![')

def test_strategy_performance_chart():
    strategy_pnls = {"A": 100, "B": -50, "C": 200}
    md = ChartGenerator.strategy_performance_chart(strategy_pnls)
    assert md.startswith('![')

def test_dte_chart():
    dte_buckets = {"0-7": 0.1, "8-30": 0.2, "31-60": -0.05, "60+": 0.3}
    md = ChartGenerator.dte_chart(dte_buckets)
    assert md.startswith('![')

def test_position_sizing_chart():
    sizes = [1, 2, 2, 3, 3, 3, 4, 5]
    md = ChartGenerator.position_sizing_chart(sizes)
    assert md.startswith('![')

def test_comparison_chart():
    data = {"A": [1, 2, 3], "B": [2, 1, 4]}
    md = ChartGenerator.comparison_chart(data)
    assert md.startswith('![')

def test_empty_data():
    # Should not error on empty input
    assert ChartGenerator.cumulative_pnl_chart([]).startswith('![')
    assert ChartGenerator.win_loss_ratio_chart([]).startswith('![')
    assert ChartGenerator.strategy_performance_chart({}).startswith('![')
    assert ChartGenerator.dte_chart({}).startswith('![')
    assert ChartGenerator.position_sizing_chart([]).startswith('![')
    assert ChartGenerator.comparison_chart({}).startswith('![') 