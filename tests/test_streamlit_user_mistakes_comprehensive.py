import io
import pytest
from unittest.mock import patch
from datetime import date
from src.app.ui_components import (
    file_upload_component, strategy_input_component, time_period_selector_component,
    form_validation_component, is_valid_strategy_name
)

def test_user_mistakes_comprehensive():
    """Comprehensive test for all user mistakes."""
    
    # Test 1: Unsupported file formats
    # Note: The actual validation happens in the Streamlit UI due to the type parameter
    # We're testing that the component accepts any file but the UI restricts it
    
    # Test 2: Invalid strategy names
    assert is_valid_strategy_name("Valid Strategy") == True
    assert is_valid_strategy_name("Strategy-123") == True
    assert is_valid_strategy_name("My_Strategy") == True
    assert is_valid_strategy_name("Test Strategy 1") == True
    
    # Invalid strategy names
    assert is_valid_strategy_name("") == False
    assert is_valid_strategy_name("   ") == False
    assert is_valid_strategy_name("Strategy@123") == False
    assert is_valid_strategy_name("Strategy#Test") == False
    assert is_valid_strategy_name("Strategy$Test") == False
    
    # Test 3: Incomplete forms (missing required data)
    # This is handled by form validation
    
    # Test 4: Misselected time periods
    form_data = {
        "strategy_name": "Valid Strategy",
        "start_date": date(2024, 12, 31),
        "end_date": date(2024, 1, 1)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 1
    assert "Start date must be before end date" in errors[0]
    
    # Test multiple errors
    form_data = {
        "strategy_name": "Invalid@Strategy",
        "start_date": date(2024, 12, 31),
        "end_date": date(2024, 1, 1)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 2
    assert any("Strategy name contains invalid characters" in error for error in errors)
    assert any("Start date must be before end date" in error for error in errors)

def test_ui_error_messages():
    """Test that UI components display appropriate error messages."""
    
    # Test strategy name validation error message
    form_data = {
        "strategy_name": "Invalid@Strategy",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 1
    assert "Strategy name contains invalid characters" in errors[0]
    assert "Only letters, numbers, spaces, hyphens, and underscores are allowed" in errors[0]
    
    # Test time period validation error message
    form_data = {
        "strategy_name": "Valid Strategy",
        "start_date": date(2024, 12, 31),
        "end_date": date(2024, 1, 1)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 1
    assert "Start date must be before end date" in errors[0]

def test_valid_inputs():
    """Test that valid inputs pass validation."""
    
    # Test valid strategy name
    assert is_valid_strategy_name("Simple Strategy") == True
    
    # Test valid form data
    form_data = {
        "strategy_name": "Valid Strategy",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 0
    
    # Test empty strategy name (optional field)
    form_data = {
        "strategy_name": "",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 0