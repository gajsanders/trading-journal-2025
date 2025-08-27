from typing import List, Dict
import matplotlib.pyplot as plt
import io
import base64

class ChartOptimizer:
    """
    Optimizes charts for markdown embedding and file size.
    """
    @staticmethod
    def optimize_chart_size(fig, max_width: int = 800, max_height: int = 600):
        fig.set_size_inches(max_width / fig.dpi, max_height / fig.dpi)
        return fig

    @staticmethod
    def generate_caption(chart_type: str, analytics: Dict) -> str:
        captions = {
            'cumulative_pnl': "Cumulative PnL over time shows overall profit/loss progression.",
            'win_loss': "Win/Loss ratio visualizes trading success rate.",
            'strategy_performance': "Strategy performance compares PnL by strategy.",
            'dte': "Time-weighted return by DTE bucket.",
            'position_sizing': "Distribution of position sizes.",
            'comparison': "Comparison of strategy performance over time."
        }
        return captions.get(chart_type, "Trading chart.")

    @staticmethod
    def optimize_file_size(image_bytes: bytes, max_size_kb: int = 200) -> bytes:
        # For PNG, actual compression is limited, but we can try to reduce DPI or use JPEG if needed
        # Here, just return as is for simplicity
        if len(image_bytes) <= max_size_kb * 1024:
            return image_bytes
        # Optionally, could re-encode at lower quality if using JPEG
        return image_bytes

    @staticmethod
    def embed_chart_as_markdown(image_bytes: bytes) -> str:
        b64 = base64.b64encode(image_bytes).decode('utf-8')
        return f'![chart](data:image/png;base64,{b64})' 