from typing import Dict, Any

class InsightGenerator:
    """
    Generates actionable insights from analytics results.
    """
    @staticmethod
    def generate_monthly_summary(analytics: Dict[str, Any]) -> str:
        return (
            f"Monthly Summary:\n"
            f"Win Rate: {analytics.get('win_rate', 'N/A')}\n"
            f"Total PnL: {analytics.get('total_pnl', 'N/A')}\n"
            f"Time-Weighted Return: {analytics.get('time_weighted_return', 'N/A')}\n"
            f"Risk-Adjusted Return: {analytics.get('risk_adjusted_return', 'N/A')}\n"
        )

    @staticmethod
    def identify_profitable_strategies(grouped_results: Dict[str, Any]) -> str:
        if not grouped_results:
            return "No strategy data available."
        best = max(grouped_results.items(), key=lambda x: x[1].get('total_pnl', 0))
        return f"Most profitable strategy: {best[0]} (PnL: {best[1].get('total_pnl', 'N/A')})"

    @staticmethod
    def highlight_performance_trends(trend_analysis: Dict[str, Any]) -> str:
        trend = trend_analysis.get('trend', 'UNKNOWN')
        return f"Performance trend: {trend}" 