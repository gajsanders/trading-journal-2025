import pytest
import os
from pathlib import Path
from src.processors.csv_processor import CSVProcessor

def test_file_not_found():
    """Test that FileNotFoundError is raised when file doesn't exist."""
    non_existent_path = "non_existent_file.csv"
    processor = CSVProcessor(non_existent_path)
    
    with pytest.raises(FileNotFoundError) as exc_info:
        processor.load_csv()
    
    assert f"File not found: '{non_existent_path}'" in str(exc_info.value)

def test_file_not_found_with_empty_path():
    """Test that FileNotFoundError is raised when empty path is provided."""
    empty_path = ""
    processor = CSVProcessor(empty_path)
    
    with pytest.raises(FileNotFoundError) as exc_info:
        processor.load_csv()
    
    assert "File not found: ''" in str(exc_info.value)

def test_file_not_found_with_non_existent_directory():
    """Test that FileNotFoundError is raised when file is in non-existent directory."""
    non_existent_dir = "non_existent_dir/file.csv"
    processor = CSVProcessor(non_existent_dir)
    
    with pytest.raises(FileNotFoundError) as exc_info:
        processor.load_csv()
    
    assert f"File not found: '{non_existent_dir}'" in str(exc_info.value)

def test_permission_denied():
    """Test that PermissionError is raised when file exists but can't be read."""
    # Create a temporary file
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "test.csv"
    
    # Create the file
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\nAAPL,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1")
    
    # Make the file read-only
    os.chmod(test_file, 0o444)  # Read-only
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(PermissionError) as exc_info:
        processor.load_csv()
    
    assert f"Permission denied: cannot read '{test_file}'" in str(exc_info.value)
    
    # Clean up
    os.chmod(test_file, 0o644)  # Restore write permissions
    test_file.unlink()
    temp_dir.rmdir()

def test_permission_denied_with_empty_path():
    """Test that PermissionError is raised when empty path is provided."""
    empty_path = ""
    processor = CSVProcessor(empty_path)
    
    with pytest.raises(FileNotFoundError) as exc_info:
        processor.load_csv()
    
    assert "File not found: ''" in str(exc_info.value)

def test_permission_denied_with_non_existent_directory():
    """Test that PermissionError is raised when file is in non-existent directory."""
    non_existent_dir = "non_existent_dir/file.csv"
    processor = CSVProcessor(non_existent_dir)
    
    with pytest.raises(FileNotFoundError) as exc_info:
        processor.load_csv()
    
    assert f"File not found: '{non_existent_dir}'" in str(exc_info.value)

def test_malformed_csv_invalid_headers():
    """Test that ValueError is raised with descriptive message for invalid headers."""
    # Create a CSV with invalid headers
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "malformed.csv"
    
    # Create CSV with missing required columns
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side\nAAPL,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO")
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(ValueError) as exc_info:
        processor.load_csv()
    
    assert "Missing required columns: ['Quantity']" in str(exc_info.value)
    
    # Clean up
    test_file.unlink()
    temp_dir.rmdir()

def test_malformed_csv_incorrect_formatting():
    """Test that ValueError is raised with descriptive message for incorrect formatting."""
    # Create a CSV with incorrect formatting (missing required field)
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "malformed.csv"
    
    # Create CSV with missing required field
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\nAAPL,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,")
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(ValueError) as exc_info:
        processor.load_csv()
    
    assert "Missing value for required field 'Quantity' in row 0" in str(exc_info.value)
    
    # Clean up
    test_file.unlink()
    temp_dir.rmdir()

def test_malformed_csv_missing_required_fields():
    """Test that ValueError is raised with descriptive message for missing required fields."""
    # Create a CSV with missing required fields
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "malformed.csv"
    
    # Create CSV with missing required fields
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n,,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1")
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(ValueError) as exc_info:
        processor.load_csv()
    
    assert "Missing value for required field 'Symbol' in row 0" in str(exc_info.value)
    
    # Clean up
    test_file.unlink()
    temp_dir.rmdir()

def test_malformed_csv_inconsistent_delimiters():
    """Test that ValueError is raised with descriptive message for inconsistent delimiters."""
    # Create a CSV with inconsistent delimiters
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "malformed.csv"
    
    # Create CSV with inconsistent delimiters
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\nAAPL,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1\nAAPL;2.5;2024-07-01 09:30;123;desc;2024-07-19;150.0;Call;BTO;1")
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(ValueError) as exc_info:
        processor.load_csv()
    
    # The error message will be from pandas, but we want to ensure it's descriptive
    assert "Failed to read CSV" in str(exc_info.value)
    
    # Clean up
    test_file.unlink()
    temp_dir.rmdir()

def test_malformed_csv_corrupted_data():
    """Test that ValueError is raised with descriptive message for corrupted data."""
    # Create a CSV with corrupted data
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "malformed.csv"
    
    # Create CSV with corrupted data
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\nAAPL,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1\nAAPL,invalid_price,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1")
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(ValueError) as exc_info:
        processor.load_csv()
    
    # The error message will be from pandas, but we want to ensure it's descriptive
    assert "Failed to read CSV" in str(exc_info.value)
    
    # Clean up
    test_file.unlink()
def test_invalid_symbol():
    """Test that ValueError is raised for invalid symbols."""
    # Create a CSV with an invalid symbol
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "invalid_symbol.csv"
    
    # Create CSV with invalid symbol
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\nINVALID,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1")
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(ValueError) as exc_info:
        processor.to_trades()
    
    assert "Trade validation failed for row 0" in str(exc_info.value)
    
    # Clean up
    test_file.unlink()
    temp_dir.rmdir()

def test_inconsistent_timestamp():
    """Test that ValueError is raised for inconsistent timestamps."""
    # Create a CSV with an invalid timestamp format
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "invalid_timestamp.csv"
    
    # Create CSV with invalid timestamp format
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\nAAPL,2.5,invalid_time,123,desc,2024-07-19,150.0,Call,BTO,1")
    
    processor = CSVProcessor(str(test_file))
    
    with pytest.raises(ValueError) as exc_info:
        processor.to_trades()
    
    assert "Trade validation failed for row 0" in str(exc_info.value)
    
    # Clean up
    test_file.unlink()
    temp_dir.rmdir()

def test_duplicate_order_numbers():
    """Test that ValueError is raised for duplicate order numbers."""
    # Create a CSV with duplicate order numbers
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(exist_ok=True)
    test_file = temp_dir / "duplicate_order.csv"

    # Create CSV with duplicate order numbers
    test_file.write_text("Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\nAAPL,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1\nAAPL,2.5,2024-07-01 09:30,123,desc,2024-07-19,150.0,Call,BTO,1")

    processor = CSVProcessor(str(test_file))

    with pytest.raises(ValueError) as exc_info:
        processor.to_trades()

    assert "Duplicate order number '123' in row 1" in str(exc_info.value)

    # Clean up
    test_file.unlink()
    temp_dir.rmdir()
    temp_dir.rmdir()