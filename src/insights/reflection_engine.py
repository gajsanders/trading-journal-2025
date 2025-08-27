from typing import Dict, Any, List
from src.llm.openai_client import OpenAIClient

class ReflectionEngine:
    """
    Generates dynamic reflection questions based on analytics and LLM.
    """
    @staticmethod
    def generate_questions(analytics: Dict[str, Any], llm_client: OpenAIClient) -> List[str]:
        prompt = (
            f"Based on these metrics, generate 3-5 personalized reflection questions to help the trader improve:\n"
            f"Win Rate: {analytics.get('win_rate', 'N/A')}\n"
            f"Total PnL: {analytics.get('total_pnl', 'N/A')}\n"
            f"Time-Weighted Return: {analytics.get('time_weighted_return', 'N/A')}\n"
            f"Risk-Adjusted Return: {analytics.get('risk_adjusted_return', 'N/A')}\n"
        )
        response = llm_client._call_openai(prompt)
        return [q.strip() for q in response.split('\n') if q.strip()]

    @staticmethod
    def question_templates() -> List[str]:
        return [
            "What was your most effective strategy this month and why?",
            "How did your risk management decisions impact your results?",
            "What patterns do you notice in your winning and losing trades?",
            "How did market conditions influence your performance?",
            "What will you focus on improving next month?"
        ] 