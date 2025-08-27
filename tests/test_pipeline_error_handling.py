import pytest
import tempfile
import os
from unittest.mock import patch
from src.processors.csv_processor import CSVProcessor
from src.visualizations.chart_generator import ChartGenerator

def test_file_not_found_error():
    # Test that file not found errors are handled gracefully
    processor = CSVProcessor("nonexistent_file.csv")
    with pytest.raises(FileNotFoundError) as exc_info:
        processor.load_csv()
    
    # Verify the error message is appropriate
    assert "File not found" in str(exc_info.value)

def test_csv_parsing_failure_handling():
    # Test that CSV parsing failures are handled gracefully with proper error messages
    # Create a CSV file with missing required columns
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write("Symbol,Price\nAAPL,150.0")
        tmp_file_path = tmp_file.name
    
    try:
        processor = CSVProcessor(tmp_file_path)
        with pytest.raises(ValueError) as exc_info:
            processor.load_csv()
        
        # Verify the error message is appropriate
        assert "Missing required columns" in str(exc_info.value)
    finally:
        os.unlink(tmp_file_path)

def test_invalid_csv_format():
    # Test that truly invalid CSV format is handled gracefully
    # Create a file that causes pandas to raise an exception
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        # Write content that causes pandas to fail
        tmp_file.write("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n")
        tmp_file.write("This line is fine\n")
        tmp_file.write("This line has too many fields,field2,field3,field4,field5,field6,field7,field8,field9,field10,extra_field\n")
        tmp_file_path = tmp_file.name
    
    try:
        processor = CSVProcessor(tmp_file_path)
        with pytest.raises(ValueError) as exc_info:
            processor.load_csv()
        
        # Verify the error message is appropriate
        assert "Failed to read CSV" in str(exc_info.value)
    finally:
        os.unlink(tmp_file_path)

def test_permission_error():
    # Test that permission errors are handled gracefully
    # Create a temporary file and make it unreadable
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n")
        tmp_file_path = tmp_file.name
    
    try:
        # Make file unreadable
        os.chmod(tmp_file_path, 0o000)
        processor = CSVProcessor(tmp_file_path)
        with pytest.raises(PermissionError) as exc_info:
            processor.load_csv()
        
        # Verify the error message is appropriate
        assert "Permission denied" in str(exc_info.value)
    finally:
        os.chmod(tmp_file_path, 0o644)  # Restore permissions
        os.unlink(tmp_file_path)

def test_malformed_row_handling():
    # Test that malformed rows are handled gracefully
    # Create a CSV file with a malformed row (invalid price)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n")
        tmp_file.write("AAPL,invalid_price,2024-01-01 10:00,123,Buy call,2024-01-19,150.0,Call,BTO,1\n")
        tmp_file.write("MSFT,1.8,2024-01-01 11:00,456,Buy put,2024-01-19,300.0,Put,BTO,2\n")
        tmp_file_path = tmp_file.name
    
    try:
        processor = CSVProcessor(tmp_file_path)
        processor.load_csv()
        trades = processor.to_trades()
        
        # Should skip the malformed row and process the valid one
        assert len(trades) == 1
        assert trades[0].symbol == "MSFT"
    finally:
        os.unlink(tmp_file_path)

def test_duplicate_order_error():
    # Test that duplicate order errors are handled gracefully
    # Create a CSV file with duplicate order numbers
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n")
        tmp_file.write("AAPL,2.5,2024-01-01 10:00,123,Buy call,2024-01-19,150.0,Call,BTO,1\n")
        tmp_file.write("MSFT,1.8,2024-01-01 11:00,123,Buy put,2024-01-19,300.0,Put,BTO,2\n")
        tmp_file_path = tmp_file.name
    
    try:
        processor = CSVProcessor(tmp_file_path)
        processor.load_csv()
        trades = processor.to_trades()
        
        # Should process only the first order (duplicates are skipped)
        assert len(trades) == 1
        assert trades[0].symbol == "AAPL"
    finally:
        os.unlink(tmp_file_path)

def test_invalid_symbol_error():
    # Test that invalid symbol errors are handled gracefully
    # Create a CSV file with an invalid symbol
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n")
        tmp_file.write("INVALID123,2.5,2024-01-01 10:00,123,Buy call,2024-01-19,150.0,Call,BTO,1\n")
        tmp_file.write("MSFT,1.8,2024-01-01 11:00,456,Buy put,2024-01-19,300.0,Put,BTO,2\n")
        tmp_file_path = tmp_file.name
    
    try:
        processor = CSVProcessor(tmp_file_path)
        processor.load_csv()
        trades = processor.to_trades()
        
        # Should skip the invalid symbol row and process the valid one
        assert len(trades) == 1
        assert trades[0].symbol == "MSFT"
    finally:
        os.unlink(tmp_file_path)

def test_invalid_timestamp_error():
    # Test that invalid timestamp errors are handled gracefully
    # Create a CSV file with an invalid timestamp
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n")
        tmp_file.write("AAPL,2.5,2024-13-45 25:70,123,Buy call,2024-01-19,150.0,Call,BTO,1\n")
        tmp_file.write("MSFT,1.8,2024-01-01 11:00,456,Buy put,2024-01-19,300.0,Put,BTO,2\n")
        tmp_file_path = tmp_file.name
    
    try:
        processor = CSVProcessor(tmp_file_path)
        processor.load_csv()
        trades = processor.to_trades()
        
        # Should skip the invalid timestamp row and process the valid one
        assert len(trades) == 1
        assert trades[0].symbol == "MSFT"
    finally:
        os.unlink(tmp_file_path)

def test_chart_generation_failure_handling():
    # Test that chart generation failures are handled gracefully with proper error messages
    # Mock matplotlib to raise an exception
    with patch('matplotlib.pyplot.plot', side_effect=Exception("Matplotlib backend error")):
        with pytest.raises(Exception) as exc_info:
            ChartGenerator.cumulative_pnl_chart([1.0, 2.0, 3.0])
        
        # Verify the error message is appropriate
        assert "Matplotlib backend error" in str(exc_info.value)

def test_chart_save_failure():
    # Test that chart save failures are handled gracefully
    # Mock file operation to raise an exception
    with patch('builtins.open', side_effect=IOError("Disk full")):
        with pytest.raises(IOError) as exc_info:
            ChartGenerator.cumulative_pnl_chart([1.0, 2.0, 3.0], save_path="/invalid/path/chart.png")
        
        # Verify the error message is appropriate
        assert "Disk full" in str(exc_info.value)