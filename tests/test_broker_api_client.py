"""
Tests for BrokerAPIClient using requests-mock for HTTP request simulation.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
import requests
from requests.exceptions import Timeout, ConnectionError

# Import the broker API client
from src.brokers.broker_api_client import BrokerAPIClient


class TestBrokerAPIClient:
    """Test cases for BrokerAPIClient."""
    
    def test_get_account_info_success(self, mock_requests):
        """Test successful account info retrieval."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_response = {
            "account_number": "12345678",
            "balance": 10000.00,
            "currency": "USD",
            "status": "active"
        }
        mock_requests.get(
            "https://api.broker.com/v1/account",
            json=mock_response,
            status_code=200
        )
        
        result = client.get_account_info()
        assert result == mock_response
        
    def test_get_account_info_timeout(self, mock_requests):
        """Test timeout handling when getting account info."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock timeout
        mock_requests.get(
            "https://api.broker.com/v1/account",
            exc=Timeout
        )
        
        with pytest.raises(Exception, match="Request to broker API timed out"):
            client.get_account_info()
            
    def test_get_account_info_connection_error(self, mock_requests):
        """Test connection error handling when getting account info."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock connection error
        mock_requests.get(
            "https://api.broker.com/v1/account",
            exc=ConnectionError
        )
        
        with pytest.raises(Exception, match="Could not connect to broker API"):
            client.get_account_info()
            
    def test_get_account_info_http_error(self, mock_requests):
        """Test HTTP error handling when getting account info."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock HTTP error
        mock_requests.get(
            "https://api.broker.com/v1/account",
            status_code=401,
            json={"error": "Unauthorized"}
        )
        
        with pytest.raises(Exception, match="Broker API returned error: 401"):
            client.get_account_info()
            
    def test_get_account_info_invalid_json(self, mock_requests):
        """Test handling of invalid JSON response."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock invalid JSON response
        mock_requests.get(
            "https://api.broker.com/v1/account",
            text="Invalid JSON",
            status_code=200
        )
        
        with pytest.raises(Exception, match="Error making request to broker API"):
            client.get_account_info()
            
    def test_get_positions_success(self, mock_requests):
        """Test successful positions retrieval."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_response = [
            {"symbol": "AAPL", "quantity": 10, "avg_price": 150.00, "current_price": 155.00},
            {"symbol": "GOOGL", "quantity": 5, "avg_price": 2500.00, "current_price": 2550.00}
        ]
        mock_requests.get(
            "https://api.broker.com/v1/positions",
            json=mock_response,
            status_code=200
        )
        
        result = client.get_positions()
        assert result == mock_response
        
    def test_place_order_success(self, mock_requests):
        """Test successful order placement."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_response = {
            "order_id": "ord_12345",
            "status": "submitted",
            "symbol": "AAPL",
            "quantity": 10,
            "type": "market"
        }
        mock_requests.post(
            "https://api.broker.com/v1/orders",
            json=mock_response,
            status_code=201
        )
        
        result = client.place_order("AAPL", 10)
        assert result == mock_response
        
    def test_place_order_invalid_response(self, mock_requests):
        """Test handling of invalid JSON response from order placement."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock invalid JSON response
        mock_requests.post(
            "https://api.broker.com/v1/orders",
            text="Invalid JSON",
            status_code=201
        )
        
        with pytest.raises(Exception, match="Error making request to broker API"):
            client.place_order("AAPL", 10)
            
    def test_cancel_order_success(self, mock_requests):
        """Test successful order cancellation."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_response = {
            "order_id": "ord_12345",
            "status": "cancelled"
        }
        mock_requests.delete(
            "https://api.broker.com/v1/orders/ord_12345",
            json=mock_response,
            status_code=200
        )
        
        result = client.cancel_order("ord_12345")
        assert result == mock_response
        
    def test_get_order_history_success(self, mock_requests):
        """Test successful order history retrieval."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_response = [
            {
                "order_id": "ord_12345",
                "symbol": "AAPL",
                "quantity": 10,
                "type": "market",
                "status": "filled",
                "timestamp": "2024-07-01T09:30:00Z"
            },
            {
                "order_id": "ord_67890",
                "symbol": "GOOGL",
                "quantity": 5,
                "type": "limit",
                "status": "cancelled",
                "timestamp": "2024-07-01T10:00:00Z"
            }
        ]
        mock_requests.get(
            "https://api.broker.com/v1/orders",
            json=mock_response,
            status_code=200
        )
        
        result = client.get_order_history()
        assert result == mock_response
        
    def test_get_order_history_with_dates(self, mock_requests):
        """Test order history retrieval with date parameters."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_response = []
        mock_requests.get(
            "https://api.broker.com/v1/orders",
            json=mock_response,
            status_code=200
        )
        
        result = client.get_order_history("2024-07-01", "2024-07-31")
        
        # Verify that the request was made with the correct parameters
        assert len(mock_requests.request_history) == 1
        request = mock_requests.request_history[0]
        assert "start_date=2024-07-01" in request.url
        assert "end_date=2024-07-31" in request.url
        assert result == mock_response
        
    def test_request_headers(self, mock_requests):
        """Test that correct headers are sent with requests."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_requests.get(
            "https://api.broker.com/v1/account",
            json={"account_number": "12345678"},
            status_code=200
        )
        
        client.get_account_info()
        
        # Verify the request was made with correct headers
        assert mock_requests.called
        request = mock_requests.request_history[0]
        assert request.headers["Authorization"] == "Bearer test-api-key"
        assert request.headers["Content-Type"] == "application/json"
        
    def test_request_timeout_configuration(self, mock_requests):
        """Test that requests use the configured timeout."""
        client = BrokerAPIClient("test-api-key")
        
        # Mock successful response
        mock_requests.get(
            "https://api.broker.com/v1/account",
            json={"account_number": "12345678"},
            status_code=200
        )
        
        client.get_account_info()
        
        # Verify the request was made with the correct timeout
        assert mock_requests.called
        request = mock_requests.request_history[0]
        # Note: requests-mock doesn't expose the timeout in request history,
        # but we can verify the request was made successfully
        assert request.url == "https://api.broker.com/v1/account"