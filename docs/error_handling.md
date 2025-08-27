# Pipeline Error Handling

## Overview

The Trading Journal application includes comprehensive error handling throughout the entire pipeline to ensure that failures are gracefully handled and users receive clear, actionable error messages.

## Error Handling Mechanisms

### 1. Input File Validation

The CSV processor validates input files at multiple levels:

- **File existence**: Checks if the file exists
- **File permissions**: Verifies read permissions
- **CSV format**: Validates that the file can be parsed as CSV
- **Required columns**: Ensures all required columns are present
- **Row validation**: Validates each row for proper data formats

### 2. Data Processing Errors

During data processing, the application handles:

- **Malformed rows**: Skips rows with invalid data formats
- **Duplicate orders**: Prevents duplicate order processing
- **Invalid symbols**: Rejects symbols that don't match expected patterns
- **Invalid timestamps**: Handles malformed date/time values
- **Data type errors**: Manages conversion failures for numeric values

### 3. Analysis Failures

The analysis pipeline handles:

- **Trade linking errors**: Manages failures in linking related trades
- **Calculation errors**: Handles mathematical errors in performance calculations
- **Invalid data ranges**: Manages edge cases in data analysis

### 4. Chart Generation Errors

Chart generation handles:

- **Backend failures**: Manages matplotlib rendering errors
- **Save failures**: Handles disk write errors
- **Data validation**: Manages invalid data for chart creation

## Error Message Design

All error messages follow these principles:

1. **Clear and specific**: Error messages clearly identify what went wrong
2. **Actionable**: Messages suggest how to fix the issue
3. **Contextual**: Include relevant context like file names, row numbers, or data values
4. **User-friendly**: Avoid technical jargon when possible

## Common Error Scenarios

### File Not Found
```
FileNotFoundError: File not found: 'trades.csv'
```
**Solution**: Verify the file path is correct and the file exists.

### Missing Required Columns
```
ValueError: Missing required columns: ['Time', 'Order #']
```
**Solution**: Ensure the CSV file contains all required columns.

### Invalid CSV Format
```
ValueError: Failed to read CSV: Error tokenizing data
```
**Solution**: Check that the CSV file is properly formatted with consistent delimiters.

### Permission Denied
```
PermissionError: Permission denied: cannot read 'protected.csv'
```
**Solution**: Check file permissions and ensure the application has read access.

### Malformed Data
```
ValueError: Invalid timestamp format '2024-13-45 25:70' in row 3
```
**Solution**: Correct the timestamp format to YYYY-MM-DD HH:MM.

### Duplicate Orders
```
ValueError: Duplicate order number '123' in row 5
```
**Solution**: Remove or correct duplicate order entries.

### Invalid Symbols
```
ValueError: Invalid symbol 'INVALID123' in row 2
```
**Solution**: Use valid stock symbols (1-5 uppercase letters).

### Chart Generation Failures
```
Exception: Matplotlib backend error
```
**Solution**: Check matplotlib installation and system graphics libraries.

### Save Failures
```
IOError: Disk full
```
**Solution**: Free up disk space or specify a different save location.

## Testing Error Conditions

The test suite includes comprehensive tests for all error conditions:

- `test_file_not_found_error()`: Tests file not found handling
- `test_csv_parsing_failure_handling()`: Tests CSV parsing failures
- `test_invalid_csv_format()`: Tests invalid CSV format handling
- `test_permission_error()`: Tests permission denied errors
- `test_malformed_row_handling()`: Tests malformed row handling
- `test_duplicate_order_error()`: Tests duplicate order handling
- `test_invalid_symbol_error()`: Tests invalid symbol handling
- `test_invalid_timestamp_error()`: Tests invalid timestamp handling
- `test_chart_generation_failure_handling()`: Tests chart generation failures
- `test_chart_save_failure()`: Tests chart save failures

Each test verifies that:
1. The appropriate exception is raised
2. The error message contains relevant information
3. The application continues to function after the error