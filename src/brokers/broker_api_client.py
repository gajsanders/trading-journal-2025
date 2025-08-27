"""
Example Broker API Client for interacting with a brokerage API.
This is an example implementation showing how to structure HTTP clients
that can be properly tested with requests-mock.
"""

import requests
from requests.exceptions import Timeout, ConnectionError
from typing import Dict, Any, List, Optional


class BrokerAPIClient:
    """
    Client for interacting with a broker API.
    
    This class demonstrates proper HTTP request handling with:
    - Proper error handling for timeouts, connection errors, and HTTP errors
    - Authorization headers
    - JSON request/response handling
    - Timeout configuration
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.broker.com/v1"):
        """
        Initialize the broker API client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the broker API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the broker API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (e.g., "/account", "/positions")
            **kwargs: Additional arguments to pass to requests.request()
            
        Returns:
            JSON response from the API
            
        Raises:
            Exception: If the request fails for any reason
        """
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f"Bearer {self.api_key}"
        headers['Content-Type'] = 'application/json'
        
        # Set default timeout if not provided
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 10
            
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except Timeout:
            raise Exception("Request to broker API timed out")
        except ConnectionError:
            raise Exception("Could not connect to broker API")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Broker API returned error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request to broker API: {str(e)}")
        except ValueError as e:
            # JSON decoding error
            raise Exception(f"Invalid JSON response from broker API: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error when communicating with broker API: {str(e)}")
            
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information from broker API.
        
        Returns:
            Account information
            
        Raises:
            Exception: If the request fails
        """
        return self._make_request("GET", "/account")
        
    def get_positions(self) -> List[Dict[str, Any]]:
        """
        Get current positions from broker API.
        
        Returns:
            List of positions
            
        Raises:
            Exception: If the request fails
        """
        return self._make_request("GET", "/positions")
        
    def place_order(self, symbol: str, quantity: int, order_type: str = "market") -> Dict[str, Any]:
        """
        Place an order through broker API.
        
        Args:
            symbol: Symbol to trade
            quantity: Number of shares/contracts
            order_type: Type of order (market, limit, etc.)
            
        Returns:
            Order details
            
        Raises:
            Exception: If the request fails
        """
        data = {
            "symbol": symbol,
            "quantity": quantity,
            "type": order_type
        }
        return self._make_request("POST", "/orders", json=data)
        
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """
        Cancel an order through broker API.
        
        Args:
            order_id: ID of the order to cancel
            
        Returns:
            Cancellation details
            
        Raises:
            Exception: If the request fails
        """
        return self._make_request("DELETE", f"/orders/{order_id}")
        
    def get_order_history(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get order history from broker API.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (optional)
            end_date: End date in YYYY-MM-DD format (optional)
            
        Returns:
            List of orders
            
        Raises:
            Exception: If the request fails
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        return self._make_request("GET", "/orders", params=params)