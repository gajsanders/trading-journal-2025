import os
import base64
from src.visualizations.chart_coordinator import ChartCoordinator
from src.visualizations.chart_optimizer import ChartOptimizer

def test_generate_all_charts(tmp_path):
    analytics = {
        'pnl_series': [10, -5, 20],
        'win_loss': [True, False, True],
        'strategy_pnls': {'A': 100, 'B': -50},
        'dte_buckets': {'0-7': 0.1, '8-30': 0.2},
        'position_sizes': [1, 2, 3],
        'comparison_data': {'A': [1, 2], 'B': [2, 1]}
    }
    save_dir = tmp_path
    charts = ChartCoordinator.generate_all_charts(analytics, save_dir=str(save_dir))
    assert set(charts.keys()) == {'cumulative_pnl', 'win_loss', 'strategy_performance', 'dte', 'position_sizing', 'comparison'}
    for k, v in charts.items():
        assert os.path.exists(v)

def test_generate_all_charts_embedded():
    analytics = {
        'pnl_series': [10, -5, 20],
        'win_loss': [True, False, True],
        'strategy_pnls': {'A': 100, 'B': -50},
        'dte_buckets': {'0-7': 0.1, '8-30': 0.2},
        'position_sizes': [1, 2, 3],
        'comparison_data': {'A': [1, 2], 'B': [2, 1]}
    }
    charts = ChartCoordinator.generate_all_charts(analytics)
    for v in charts.values():
        assert v.startswith('![')

def test_generate_caption():
    analytics = {}
    assert "Cumulative PnL" in ChartOptimizer.generate_caption('cumulative_pnl', analytics)
    assert "Win/Loss" in ChartOptimizer.generate_caption('win_loss', analytics)
    assert "Trading chart" in ChartOptimizer.generate_caption('unknown', analytics)

def test_optimize_file_size():
    # Just test passthrough for small image
    data = b'12345' * 100
    out = ChartOptimizer.optimize_file_size(data, max_size_kb=1)
    assert out == data

def test_embed_chart_as_markdown():
    data = b'12345' * 100
    md = ChartOptimizer.embed_chart_as_markdown(data)
    assert md.startswith('![')
    assert 'base64' in md 