import pytest
from unittest.mock import patch, MagicMock
from src.llm.prompt_builder import PromptBuilder
from src.llm.openai_client import OpenAIClient

metrics = {
    'win_rate': 0.6,
    'total_pnl': 1000,
    'time_weighted_return': 0.12,
    'risk_adjusted_return': 1.5,
    'holding_periods': [5, 10, 15]
}

def test_build_performance_prompt():
    prompt = PromptBuilder.build_performance_prompt(metrics)
    assert "Win Rate: 0.6" in prompt
    assert "Total PnL: 1000" in prompt
    assert "Please provide a concise analysis" in prompt

def test_build_reflection_prompt():
    prompt = PromptBuilder.build_reflection_prompt(metrics)
    assert "generate 3-5 reflection questions" in prompt
    assert "Win Rate: 0.6" in prompt

def test_format_context():
    context = PromptBuilder.format_context({'foo': 'bar'})
    assert "foo" in context
    assert "Trading Data Context" in context

@patch('openai.ChatCompletion.create')
def test_generate_performance_analysis(mock_create):
    mock_create.return_value = MagicMock(choices=[MagicMock(message={"content": "Analysis result"})])
    client = OpenAIClient(api_key="test-key", rate_limit=1000)
    result = client.generate_performance_analysis(metrics)
    assert "Analysis result" in result

@patch('openai.ChatCompletion.create', side_effect=Exception("API error"))
def test_openai_api_error(mock_create):
    client = OpenAIClient(api_key="test-key", rate_limit=1000)
    result = client.generate_performance_analysis(metrics)
    assert "API error" in result

def test_rate_limiting():
    import time
    client = OpenAIClient(api_key="test-key", rate_limit=120)
    start = time.time()
    client._rate_limit()  # Should not sleep on first call
    elapsed = time.time() - start
    assert elapsed < 0.5  # Should be fast 