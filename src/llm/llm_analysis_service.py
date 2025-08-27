"""
Example LLM Analysis Service for performing LLM-based analysis of trading performance.
This is an example implementation showing how to structure HTTP clients
that can be properly tested with requests-mock.
"""

import requests
from requests.exceptions import Timeout, ConnectionError
from typing import Dict, Any, List, Optional


class LLMAnalysisService:
    """
    Service for performing LLM-based analysis of trading performance.
    
    This class demonstrates proper HTTP request handling with:
    - Proper error handling for timeouts, connection errors, and HTTP errors
    - Authorization headers
    - JSON request/response handling
    - Timeout configuration
    """
    
    def __init__(self, api_endpoint: str, api_key: Optional[str] = None, model: str = "gpt-analysis-model"):
        """
        Initialize the LLM analysis service.
        
        Args:
            api_endpoint: Endpoint for the LLM API
            api_key: API key for authentication (optional)
            model: Model to use for analysis
        """
        self.api_endpoint = api_endpoint.rstrip('/')  # Remove trailing slash if present
        self.api_key = api_key
        self.model = model
        
    def _make_request(self, prompt: str) -> Dict[str, Any]:
        """
        Make an HTTP request to the LLM API.
        
        Args:
            prompt: Prompt to send to the LLM
            
        Returns:
            JSON response from the API
            
        Raises:
            Exception: If the request fails for any reason
        """
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a trading performance analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Timeout:
            raise Exception("LLM analysis request timed out")
        except ConnectionError:
            raise Exception("Could not connect to LLM analysis service")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"LLM service returned error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request to LLM service: {str(e)}")
        except ValueError as e:
            # JSON decoding error
            raise Exception(f"Invalid JSON response from LLM service: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error during LLM analysis: {str(e)}")
            
    def analyze_trades(self, trades_data: Dict[str, Any]) -> str:
        """
        Send trades data to LLM for analysis.
        
        Args:
            trades_data: Dictionary containing trade information
            
        Returns:
            Analysis results from LLM
            
        Raises:
            Exception: If API request fails
        """
        prompt = f"Analyze these trades: {trades_data}"
        try:
            response = self._make_request(prompt)
            return response["analysis"]
        except KeyError:
            raise Exception("Invalid response format from LLM service")
        except Exception as e:
            raise Exception(f"Error analyzing trades: {str(e)}")
            
    def generate_reflection_questions(self, trades_data: Dict[str, Any]) -> List[str]:
        """
        Generate reflection questions based on trade data.
        
        Args:
            trades_data: Dictionary containing trade information
            
        Returns:
            List of reflection questions from LLM
            
        Raises:
            Exception: If API request fails
        """
        prompt = f"Generate 3-5 reflection questions based on these trades: {trades_data}"
        try:
            response = self._make_request(prompt)
            return response["questions"]
        except KeyError:
            raise Exception("Invalid response format from LLM service")
        except Exception as e:
            raise Exception(f"Error generating reflection questions: {str(e)}")
            
    def get_market_sentiment(self, symbols: List[str]) -> Dict[str, str]:
        """
        Get market sentiment for a list of symbols.
        
        Args:
            symbols: List of symbols to analyze
            
        Returns:
            Dictionary mapping symbols to sentiment analysis
            
        Raises:
            Exception: If API request fails
        """
        prompt = f"Provide market sentiment analysis for these symbols: {', '.join(symbols)}"
        try:
            response = self._make_request(prompt)
            return response["sentiment"]
        except KeyError:
            raise Exception("Invalid response format from LLM service")
        except Exception as e:
            raise Exception(f"Error getting market sentiment: {str(e)}")