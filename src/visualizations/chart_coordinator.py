from typing import Dict, Any, List
from src.visualizations.chart_generator import ChartGenerator

class ChartCoordinator:
    """
    Coordinates batch chart generation for monthly reports.
    """
    @staticmethod
    def generate_all_charts(analytics: Dict[str, Any], save_dir: str = None) -> Dict[str, str]:
        charts = {}
        charts['cumulative_pnl'] = ChartGenerator.cumulative_pnl_chart(analytics.get('pnl_series', []), save_path=(f"{save_dir}/cumulative_pnl.png" if save_dir else None))
        charts['win_loss'] = ChartGenerator.win_loss_ratio_chart(analytics.get('win_loss', []), save_path=(f"{save_dir}/win_loss.png" if save_dir else None))
        charts['strategy_performance'] = ChartGenerator.strategy_performance_chart(analytics.get('strategy_pnls', {}), save_path=(f"{save_dir}/strategy_performance.png" if save_dir else None))
        charts['dte'] = ChartGenerator.dte_chart(analytics.get('dte_buckets', {}), save_path=(f"{save_dir}/dte.png" if save_dir else None))
        charts['position_sizing'] = ChartGenerator.position_sizing_chart(analytics.get('position_sizes', []), save_path=(f"{save_dir}/position_sizing.png" if save_dir else None))
        charts['comparison'] = ChartGenerator.comparison_chart(analytics.get('comparison_data', {}), save_path=(f"{save_dir}/comparison.png" if save_dir else None))
        return charts 