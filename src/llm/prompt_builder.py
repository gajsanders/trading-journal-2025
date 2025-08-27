from typing import Dict, Any

class PromptBuilder:
    """
    Builds prompts for OpenAI API: performance analysis and reflection questions.
    """
    @staticmethod
    def build_performance_prompt(metrics: Dict[str, Any]) -> str:
        return (
            f"Performance Summary:\n"
            f"Win Rate: {metrics.get('win_rate', 'N/A')}\n"
            f"Total PnL: {metrics.get('total_pnl', 'N/A')}\n"
            f"Time-Weighted Return: {metrics.get('time_weighted_return', 'N/A')}\n"
            f"Risk-Adjusted Return: {metrics.get('risk_adjusted_return', 'N/A')}\n"
            f"Holding Periods: {metrics.get('holding_periods', [])}\n"
            f"Please provide a concise analysis of this trading performance."
        )

    @staticmethod
    def build_reflection_prompt(metrics: Dict[str, Any]) -> str:
        return (
            f"Based on the following trading metrics:\n"
            f"Win Rate: {metrics.get('win_rate', 'N/A')}\n"
            f"Total PnL: {metrics.get('total_pnl', 'N/A')}\n"
            f"Time-Weighted Return: {metrics.get('time_weighted_return', 'N/A')}\n"
            f"Risk-Adjusted Return: {metrics.get('risk_adjusted_return', 'N/A')}\n"
            f"Please generate 3-5 reflection questions to help the trader improve."
        )

    @staticmethod
    def format_context(trading_data: Dict[str, Any]) -> str:
        return f"Trading Data Context:\n{trading_data}" 