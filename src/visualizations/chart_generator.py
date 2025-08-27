import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
from src.visualizations.chart_config import apply_chart_style
import io
import base64

class ChartGenerator:
    """
    Generates charts for trading analytics and reporting.
    """
    @staticmethod
    def cumulative_pnl_chart(pnls: List[float], save_path: str = None) -> str:
        apply_chart_style()
        cum_pnl = [sum(pnls[:i+1]) for i in range(len(pnls))]
        plt.figure()
        plt.plot(cum_pnl, marker='o')
        plt.title("Cumulative PnL Over Time")
        plt.xlabel("Trade #")
        plt.ylabel("Cumulative PnL")
        plt.tight_layout()
        return ChartGenerator._save_or_embed(save_path)

    @staticmethod
    def win_loss_ratio_chart(win_loss: List[bool], save_path: str = None) -> str:
        apply_chart_style()
        win_count = sum(win_loss)
        loss_count = len(win_loss) - win_count
        plt.figure()
        plt.bar(["Wins", "Losses"], [win_count, loss_count], color=["#4CAF50", "#F44336"])
        plt.title("Win/Loss Ratio")
        plt.ylabel("Count")
        plt.tight_layout()
        return ChartGenerator._save_or_embed(save_path)

    @staticmethod
    def strategy_performance_chart(strategy_pnls: Dict[str, float], save_path: str = None) -> str:
        apply_chart_style()
        plt.figure()
        strategies = list(strategy_pnls.keys())
        pnls = list(strategy_pnls.values())
        sns.barplot(x=strategies, y=pnls)
        plt.title("Strategy Performance")
        plt.xlabel("Strategy")
        plt.ylabel("Total PnL")
        plt.tight_layout()
        return ChartGenerator._save_or_embed(save_path)

    @staticmethod
    def dte_chart(dte_buckets: Dict[str, float], save_path: str = None) -> str:
        apply_chart_style()
        plt.figure()
        buckets = list(dte_buckets.keys())
        returns = list(dte_buckets.values())
        sns.barplot(x=buckets, y=returns)
        plt.title("Time-Weighted Return by DTE Bucket")
        plt.xlabel("DTE Range (days)")
        plt.ylabel("Return")
        plt.tight_layout()
        return ChartGenerator._save_or_embed(save_path)

    @staticmethod
    def position_sizing_chart(sizes: List[float], save_path: str = None) -> str:
        apply_chart_style()
        plt.figure()
        sns.histplot(sizes, bins=10, kde=True)
        plt.title("Position Sizing Distribution")
        plt.xlabel("Position Size")
        plt.ylabel("Frequency")
        plt.tight_layout()
        return ChartGenerator._save_or_embed(save_path)

    @staticmethod
    def comparison_chart(data: Dict[str, List[float]], save_path: str = None) -> str:
        apply_chart_style()
        plt.figure()
        for label, values in data.items():
            plt.plot(values, label=label)
        plt.title("Strategy Performance Comparison")
        plt.xlabel("Trade #")
        plt.ylabel("PnL")
        plt.legend()
        plt.tight_layout()
        return ChartGenerator._save_or_embed(save_path)

    @staticmethod
    def _save_or_embed(save_path: str = None) -> str:
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        if save_path:
            with open(save_path, 'wb') as f:
                f.write(buf.getvalue())
            return save_path
        # Return as markdown-embeddable base64 string
        b64 = base64.b64encode(buf.read()).decode('utf-8')
        return f'![chart](data:image/png;base64,{b64})' 