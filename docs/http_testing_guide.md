# HTTP Request Testing Guide

This document explains how to test HTTP requests in the Trading Journal application using `requests-mock`.

## Setup

The testing environment is already configured with:
1. `requests-mock` added to `requirements.txt`
2. A `conftest.py` file with a `mock_requests` fixture

## Testing Patterns

### 1. Successful Responses

To test successful HTTP responses:

```python
def test_api_success(self, mock_requests):
    """Test successful API response."""
    # Mock a successful response
    mock_requests.get(
        "https://api.example.com/endpoint",
        json={"result": "success"},
        status_code=200
    )
    
    # Call your function that makes the HTTP request
    result = my_function_that_calls_api()
    
    # Assert expected behavior
    assert result == "success"
```

### 2. Timeout Handling

To test timeout scenarios:

```python
def test_api_timeout(self, mock_requests):
    """Test timeout handling."""
    from requests.exceptions import Timeout
    
    # Mock a timeout
    mock_requests.get(
        "https://api.example.com/endpoint",
        exc=Timeout
    )
    
    # Assert that your function handles the timeout appropriately
    with pytest.raises(Exception, match="Request timed out"):
        my_function_that_calls_api()
```

### 3. Connection Errors

To test connection errors:

```python
def test_api_connection_error(self, mock_requests):
    """Test connection error handling."""
    from requests.exceptions import ConnectionError
    
    # Mock a connection error
    mock_requests.get(
        "https://api.example.com/endpoint",
        exc=ConnectionError
    )
    
    # Assert that your function handles the connection error appropriately
    with pytest.raises(Exception, match="Could not connect"):
        my_function_that_calls_api()
```

### 4. HTTP Error Responses

To test HTTP error responses:

```python
def test_api_http_error(self, mock_requests):
    """Test HTTP error response handling."""
    # Mock an HTTP error
    mock_requests.get(
        "https://api.example.com/endpoint",
        status_code=401,
        json={"error": "Unauthorized"}
    )
    
    # Assert that your function handles the HTTP error appropriately
    with pytest.raises(Exception, match="returned error: 401"):
        my_function_that_calls_api()
```

### 5. Invalid Responses

To test invalid response formats:

```python
def test_api_invalid_response(self, mock_requests):
    """Test invalid response format handling."""
    # Mock an invalid response (missing expected fields)
    mock_requests.get(
        "https://api.example.com/endpoint",
        json={"unexpected": "format"},
        status_code=200
    )
    
    # Assert that your function handles the invalid response appropriately
    with pytest.raises(Exception, match="Invalid response format"):
        my_function_that_calls_api()
```

### 6. POST Requests

To test POST requests:

```python
def test_api_post_success(self, mock_requests):
    """Test successful POST request."""
    # Mock a successful POST response
    mock_requests.post(
        "https://api.example.com/endpoint",
        json={"id": "123", "status": "created"},
        status_code=201
    )
    
    # Call your function that makes the POST request
    result = my_function_that_posts_data({"name": "test"})
    
    # Assert expected behavior
    assert result["id"] == "123"
    assert result["status"] == "created"
```

### 7. Different HTTP Methods

You can mock any HTTP method:

```python
def test_api_put_request(self, mock_requests):
    """Test PUT request."""
    mock_requests.put(
        "https://api.example.com/endpoint/123",
        json={"id": "123", "updated": True},
        status_code=200
    )
    
    result = my_function_that_updates_resource("123", {"name": "updated"})
    assert result["updated"] is True

def test_api_delete_request(self, mock_requests):
    """Test DELETE request."""
    mock_requests.delete(
        "https://api.example.com/endpoint/123",
        status_code=204
    )
    
    result = my_function_that_deletes_resource("123")
    assert result is True
```

## Advanced Testing Patterns

### 1. Testing Request Headers

To verify that your code sends the correct headers:

```python
def test_api_with_headers(self, mock_requests):
    """Test that correct headers are sent."""
    mock_requests.get(
        "https://api.example.com/endpoint",
        json={"result": "success"},
        status_code=200
    )
    
    my_function_that_calls_api_with_auth()
    
    # Verify the request was made with correct headers
    assert mock_requests.called
    assert mock_requests.request_history[0].headers["Authorization"] == "Bearer test-token"
    assert mock_requests.request_history[0].headers["Content-Type"] == "application/json"
```

### 2. Testing Request Payload

To verify that your code sends the correct data:

```python
def test_api_with_payload(self, mock_requests):
    """Test that correct payload is sent."""
    mock_requests.post(
        "https://api.example.com/endpoint",
        json={"result": "success"},
        status_code=200
    )
    
    my_function_that_posts_data({"name": "test", "value": 42})
    
    # Verify the request was made with correct payload
    assert mock_requests.called
    request = mock_requests.request_history[0]
    assert request.json() == {"name": "test", "value": 42}
```

### 3. Sequential Requests

To test APIs that make multiple requests:

```python
def test_api_multiple_requests(self, mock_requests):
    """Test multiple sequential requests."""
    # Mock multiple responses
    mock_requests.get(
        "https://api.example.com/endpoint/1",
        json={"id": "1", "name": "first"},
        status_code=200
    )
    mock_requests.get(
        "https://api.example.com/endpoint/2",
        json={"id": "2", "name": "second"},
        status_code=200
    )
    
    results = my_function_that_fetches_multiple_resources()
    
    # Verify both requests were made
    assert len(mock_requests.request_history) == 2
    assert results[0]["id"] == "1"
    assert results[1]["id"] == "2"
```

### 4. Conditional Responses

To test different responses based on request parameters:

```python
def test_api_conditional_response(self, mock_requests):
    """Test conditional responses based on request parameters."""
    def callback(request, context):
        if "status=active" in request.url:
            context.status_code = 200
            return [{"id": "1", "status": "active"}]
        else:
            context.status_code = 200
            return []
    
    mock_requests.get(
        "https://api.example.com/endpoint",
        json=callback
    )
    
    active_items = my_function_that_filters_by_status("active")
    assert len(active_items) == 1
    assert active_items[0]["status"] == "active"
```

## Best Practices

1. **Always test error cases**: Timeout, connection errors, HTTP errors, and invalid responses
2. **Use descriptive error messages**: Make sure your application provides clear error messages to users
3. **Test both success and failure paths**: Ensure your application behaves correctly in all scenarios
4. **Mock at the HTTP level**: Use requests-mock to mock at the HTTP level rather than mocking internal functions
5. **Test with realistic data**: Use JSON responses that match what the actual API would return
6. **Verify request details**: Check that headers, payloads, and URLs are correct
7. **Test edge cases**: Empty responses, malformed JSON, unexpected status codes
8. **Keep tests isolated**: Each test should mock only what it needs

## Running Tests

To run tests with requests-mock:

```bash
pytest tests/test_my_api_client.py
```

Or run all tests:

```bash
pytest
```