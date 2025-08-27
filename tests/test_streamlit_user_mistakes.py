import pytest
from datetime import date
from src.app.ui_components import is_valid_strategy_name, form_validation_component

def test_is_valid_strategy_name():
    # Test valid strategy names
    assert is_valid_strategy_name("Simple Strategy") == True
    assert is_valid_strategy_name("Strategy-123") == True
    assert is_valid_strategy_name("My_Strategy") == True
    assert is_valid_strategy_name("Test Strategy 1") == True
    
    # Test invalid strategy names
    assert is_valid_strategy_name("") == False
    assert is_valid_strategy_name("   ") == False
    assert is_valid_strategy_name("Strategy@123") == False
    assert is_valid_strategy_name("Strategy#Test") == False
    assert is_valid_strategy_name("Strategy$Test") == False

def test_form_validation_component_valid_data():
    # Test form validation with valid data
    form_data = {
        "strategy_name": "Valid Strategy",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 0

def test_form_validation_component_invalid_strategy():
    # Test form validation with invalid strategy name
    form_data = {
        "strategy_name": "Invalid@Strategy",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 1
    assert "Strategy name contains invalid characters" in errors[0]

def test_form_validation_component_invalid_date_range():
    # Test form validation with invalid date range
    form_data = {
        "strategy_name": "Valid Strategy",
        "start_date": date(2024, 12, 31),
        "end_date": date(2024, 1, 1)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 1
    assert "Start date must be before end date" in errors[0]

def test_form_validation_component_multiple_errors():
    # Test form validation with multiple errors
    form_data = {
        "strategy_name": "Invalid@Strategy",
        "start_date": date(2024, 12, 31),
        "end_date": date(2024, 1, 1)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 2
    assert any("Strategy name contains invalid characters" in error for error in errors)
    assert any("Start date must be before end date" in error for error in errors)

def test_form_validation_component_empty_strategy():
    # Test form validation with empty strategy name (should be valid)
    form_data = {
        "strategy_name": "",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    errors = form_validation_component(form_data)
    assert len(errors) == 0