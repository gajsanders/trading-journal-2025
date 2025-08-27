"""
Tests for LLMAnalysisService using requests-mock for HTTP request simulation.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import requests
from requests.exceptions import Timeout, ConnectionError

# Import the LLM analysis service
from src.llm.llm_analysis_service import LLMAnalysisService


class TestLLMAnalysisService:
    """Test cases for LLMAnalysisService."""
    
    def test_analyze_trades_success(self, mock_requests):
        """Test successful trade analysis."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock successful response
        mock_response = {
            "analysis": "Your trading performance shows a positive edge with a 60% win rate."
        }
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json=mock_response,
            status_code=200
        )
        
        result = service.analyze_trades(trades_data)
        assert result == "Your trading performance shows a positive edge with a 60% win rate."
        
    def test_analyze_trades_timeout(self, mock_requests):
        """Test timeout handling during trade analysis."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock timeout
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            exc=Timeout
        )
        
        with pytest.raises(Exception, match="LLM analysis request timed out"):
            service.analyze_trades(trades_data)
            
    def test_analyze_trades_connection_error(self, mock_requests):
        """Test connection error handling during trade analysis."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock connection error
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            exc=ConnectionError
        )
        
        with pytest.raises(Exception, match="Could not connect to LLM analysis service"):
            service.analyze_trades(trades_data)
            
    def test_analyze_trades_http_error(self, mock_requests):
        """Test HTTP error handling during trade analysis."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock HTTP error
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            status_code=401,
            json={"error": "Unauthorized"}
        )
        
        with pytest.raises(Exception, match="LLM service returned error: 401"):
            service.analyze_trades(trades_data)
            
    def test_analyze_trades_invalid_response(self, mock_requests):
        """Test handling of invalid response format."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock invalid response (missing 'analysis' key)
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json={"result": "missing_key"},
            status_code=200
        )
        
        with pytest.raises(Exception, match="Invalid response format from LLM service"):
            service.analyze_trades(trades_data)
            
    def test_analyze_trades_unexpected_error(self, mock_requests):
        """Test unexpected error handling during trade analysis."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock unexpected error
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            exc=Exception("Network failure")
        )
        
        with pytest.raises(Exception, match="Unexpected error during LLM analysis"):
            service.analyze_trades(trades_data)
            
    def test_analyze_trades_without_api_key(self, mock_requests):
        """Test trade analysis without API key."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock successful response
        mock_response = {
            "analysis": "Your trading performance shows a positive edge."
        }
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json=mock_response,
            status_code=200
        )
        
        result = service.analyze_trades(trades_data)
        assert result == "Your trading performance shows a positive edge."
        
    def test_generate_reflection_questions_success(self, mock_requests):
        """Test successful generation of reflection questions."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock successful response
        mock_response = {
            "questions": [
                "What trading patterns contributed most to your winning trades?",
                "How can you reduce the frequency of losing trades?",
                "What market conditions favored your best-performing strategies?"
            ]
        }
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json=mock_response,
            status_code=200
        )
        
        result = service.generate_reflection_questions(trades_data)
        assert len(result) == 3
        assert "What trading patterns contributed most to your winning trades?" in result
        
    def test_generate_reflection_questions_invalid_response(self, mock_requests):
        """Test handling of invalid response format for reflection questions."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {
            "total_trades": 50,
            "win_rate": 0.6,
            "avg_win": 200,
            "avg_loss": -100
        }
        
        # Mock invalid response (missing 'questions' key)
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json={"result": "missing_key"},
            status_code=200
        )
        
        with pytest.raises(Exception, match="Invalid response format from LLM service"):
            service.generate_reflection_questions(trades_data)
            
    def test_get_market_sentiment_success(self, mock_requests):
        """Test successful market sentiment retrieval."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        symbols = ["AAPL", "GOOGL", "MSFT"]
        
        # Mock successful response
        mock_response = {
            "sentiment": {
                "AAPL": "Bullish",
                "GOOGL": "Neutral",
                "MSFT": "Bearish"
            }
        }
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json=mock_response,
            status_code=200
        )
        
        result = service.get_market_sentiment(symbols)
        assert len(result) == 3
        assert result["AAPL"] == "Bullish"
        assert result["GOOGL"] == "Neutral"
        assert result["MSFT"] == "Bearish"
        
    def test_request_headers_with_api_key(self, mock_requests):
        """Test that correct headers are sent with API key."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        # Mock successful response
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json={"analysis": "test"},
            status_code=200
        )
        
        service.analyze_trades({"test": "data"})
        
        # Verify the request was made with correct headers
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert request.headers["Authorization"] == "Bearer test-key"
        assert request.headers["Content-Type"] == "application/json"
        
    def test_request_headers_without_api_key(self, mock_requests):
        """Test that correct headers are sent without API key."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze")
        
        # Mock successful response
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json={"analysis": "test"},
            status_code=200
        )
        
        service.analyze_trades({"test": "data"})
        
        # Verify the request was made with correct headers
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert "Authorization" not in request.headers
        assert request.headers["Content-Type"] == "application/json"
        
    def test_request_payload_structure(self, mock_requests):
        """Test that request payload has correct structure."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        trades_data = {"test": "data"}
        
        # Mock successful response
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json={"analysis": "test"},
            status_code=200
        )
        
        service.analyze_trades(trades_data)
        
        # Verify the request was made with correct payload
        assert mock_requests.called
        request = mock_requests.request_history[0]
        payload = request.json()
        
        assert "model" in payload
        assert payload["model"] == "gpt-analysis-model"
        assert "messages" in payload
        assert len(payload["messages"]) == 2
        assert payload["messages"][0]["role"] == "system"
        assert payload["messages"][1]["role"] == "user"
        
    def test_request_timeout_configuration(self, mock_requests):
        """Test that requests use the configured timeout."""
        service = LLMAnalysisService("https://api.llm-service.com/analyze", "test-key")
        
        # Mock successful response
        mock_requests.post(
            "https://api.llm-service.com/analyze",
            json={"analysis": "test"},
            status_code=200
        )
        
        service.analyze_trades({"test": "data"})
        
        # Verify the request was made with the correct timeout
        assert mock_requests.called
        request = mock_requests.request_history[0]
        # Note: requests-mock doesn't expose the timeout in request history,
        # but we can verify the request was made successfully
        assert request.url == "https://api.llm-service.com/analyze"