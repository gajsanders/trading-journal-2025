import pytest
from unittest.mock import MagicMock
from src.insights.insight_generator import InsightGenerator
from src.insights.reflection_engine import ReflectionEngine

analytics = {
    'win_rate': 0.7,
    'total_pnl': 1500,
    'time_weighted_return': 0.18,
    'risk_adjusted_return': 2.1,
    'holding_periods': [5, 10, 15]
}
grouped_results = {
    'StrategyA': {'total_pnl': 1000},
    'StrategyB': {'total_pnl': 1500},
    'StrategyC': {'total_pnl': 500}
}
trend_analysis = {'trend': 'UP'}

def test_generate_monthly_summary():
    summary = InsightGenerator.generate_monthly_summary(analytics)
    assert "Win Rate: 0.7" in summary
    assert "Total PnL: 1500" in summary

def test_identify_profitable_strategies():
    result = InsightGenerator.identify_profitable_strategies(grouped_results)
    assert "StrategyB" in result
    assert "1500" in result

def test_highlight_performance_trends():
    result = InsightGenerator.highlight_performance_trends(trend_analysis)
    assert "UP" in result

def test_question_templates():
    templates = ReflectionEngine.question_templates()
    assert len(templates) >= 3
    assert any("strategy" in t.lower() for t in templates)

def test_generate_questions_llm():
    class DummyLLM:
        def _call_openai(self, prompt):
            return "Q1\nQ2\nQ3"
    questions = ReflectionEngine.generate_questions(analytics, DummyLLM())
    assert questions == ["Q1", "Q2", "Q3"] 