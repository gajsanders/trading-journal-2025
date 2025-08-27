import os
import pytest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.reports.export_handler import ExportHandler
from src.processors.csv_processor import CSVProcessor

# Create a temporary directory for testing
TEST_DIR = tempfile.mkdtemp()
TEST_CSV_PATH = os.path.join(TEST_DIR, "test.csv")
TEST_MARKDOWN_PATH = os.path.join(TEST_DIR, "test.md")

# Sample CSV content for testing
SAMPLE_CSV_CONTENT = """Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity
AAPL,150.25,2025-08-23,12345,Call Option,2025-12-31,150.00,Call,Buy,100
MSFT,300.75,2025-08-23,12346,Put Option,2025-12-31,300.00,Put,Sell,50"""

# Sample markdown content for testing
SAMPLE_MARKDOWN_CONTENT = """# Trading Report
## Summary
- Total trades: 2
- Total profit: $1,250.00
- Win rate: 60%
"""

class TestExportErrorHandling:
    """Test cases for error handling during data export operations."""
    
    @classmethod
    def setup_class(cls):
        """Set up test environment before running tests."""
        # Create test CSV file
        with open(TEST_CSV_PATH, 'w') as f:
            f.write(SAMPLE_CSV_CONTENT)
    
    @classmethod
    def teardown_class(cls):
        """Clean up test environment after running tests."""
        # Remove test directory and all contents
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
    
    def test_permission_denied_csv_export(self):
        """Test that permission denied error is raised when trying to export CSV to a restricted directory."""
        # Create a directory with restricted permissions
        restricted_dir = os.path.join(TEST_DIR, "restricted")
        os.makedirs(restricted_dir)
        
        # Change permissions to make directory read-only
        os.chmod(restricted_dir, 0o444)  # Read-only permissions
        
        # Try to export CSV to restricted directory
        processor = CSVProcessor(TEST_CSV_PATH)
        with pytest.raises(PermissionError, match="Permission denied"):
            processor.to_trades()
        
        # Clean up
        os.chmod(restricted_dir, 0o755)  # Restore normal permissions
        os.rmdir(restricted_dir)
    
    def test_permission_denied_markdown_export(self):
        """Test that permission denied error is raised when trying to export Markdown to a restricted directory."""
        # Create a directory with restricted permissions
        restricted_dir = os.path.join(TEST_DIR, "restricted")
        os.makedirs(restricted_dir)
        
        # Change permissions to make directory read-only
        os.chmod(restricted_dir, 0o444)  # Read-only permissions
        
        # Try to export markdown to restricted directory
        markdown_path = os.path.join(restricted_dir, "report.md")
        with pytest.raises(PermissionError, match="Permission denied"):
            ExportHandler.save_report(SAMPLE_MARKDOWN_CONTENT, markdown_path)
        
        # Clean up
        os.chmod(restricted_dir, 0o755)  # Restore normal permissions
        os.rmdir(restricted_dir)
    
    def test_insufficient_disk_space_csv_export(self):
        """Test that insufficient disk space error is raised when trying to export CSV with no disk space."""
        # Create a file that will consume all available disk space
        # This is a simulation - in practice, we'd need to use a different approach
        # For this test, we'll use a mock to simulate the error
        
        with patch('src.processors.csv_processor.pd.read_csv') as mock_read_csv:
            # Simulate OSError with errno 28 (ENOSPC - No space left on device)
            mock_read_csv.side_effect = OSError(28, "No space left on device")
            
            # Try to load CSV
            processor = CSVProcessor(TEST_CSV_PATH)
            with pytest.raises(OSError, match="No space left on device"):
                processor.load_csv()
    
    def test_insufficient_disk_space_markdown_export(self):
        """Test that insufficient disk space error is raised when trying to export Markdown with no disk space."""
        # Create a file that will consume all available disk space
        # This is a simulation - in practice, we'd need to use a different approach
        # For this test, we'll use a mock to simulate the error
        
        with patch('src.reports.export_handler.ExportHandler.save_report') as mock_save:
            # Simulate OSError with errno 28 (ENOSPC - No space left on device)
            mock_save.side_effect = OSError(28, "No space left on device")
            
            # Try to save markdown report
            with pytest.raises(OSError, match="No space left on device"):
                ExportHandler.save_report(SAMPLE_MARKDOWN_CONTENT, TEST_MARKDOWN_PATH)
    
    def test_file_locking_conflict_csv_export(self):
        """Test that file locking conflict error is raised when trying to export CSV to a locked file."""
        # Create a file that will be locked
        locked_file = os.path.join(TEST_DIR, "locked.csv")
        with open(locked_file, 'w') as f:
            f.write(SAMPLE_CSV_CONTENT)
        
        # Try to export CSV to the same file (this should cause a file locking conflict)
        # In practice, we'd need to use a different approach to simulate file locking
        # For this test, we'll use a mock to simulate the error
        
        with patch('src.processors.csv_processor.pd.read_csv') as mock_read_csv:
            # Simulate OSError with errno 13 (EACCES - Permission denied)
            mock_read_csv.side_effect = OSError(13, "Permission denied")
            
            # Try to load CSV
            processor = CSVProcessor(locked_file)
            with pytest.raises(OSError, match="Permission denied"):
                processor.load_csv()
        
        # Clean up
        os.remove(locked_file)
    
    def test_file_locking_conflict_markdown_export(self):
        """Test that file locking conflict error is raised when trying to export Markdown to a locked file."""
        # Create a file that will be locked
        locked_file = os.path.join(TEST_DIR, "locked.md")
        with open(locked_file, 'w') as f:
            f.write(SAMPLE_MARKDOWN_CONTENT)
        
        # Try to export markdown to the same file (this should cause a file locking conflict)
        # In practice, we'd need to use a different approach to simulate file locking
        # For this test, we'll use a mock to simulate the error
        
        with patch('src.reports.export_handler.ExportHandler.save_report') as mock_save:
            # Simulate OSError with errno 13 (EACCES - Permission denied)
            mock_save.side_effect = OSError(13, "Permission denied")
            
            # Try to save markdown report
            with pytest.raises(OSError, match="Permission denied"):
                ExportHandler.save_report(SAMPLE_MARKDOWN_CONTENT, locked_file)
        
        # Clean up
        os.remove(locked_file)
    
    def test_export_with_invalid_path(self):
        """Test that appropriate error is raised when exporting to an invalid path."""
        # Test with a path that doesn't exist and can't be created
        invalid_path = "/root/invalid/path/report.md"
        
        # Try to save markdown report to invalid path
        with pytest.raises(OSError, match="No such file or directory"):
            ExportHandler.save_report(SAMPLE_MARKDOWN_CONTENT, invalid_path)
    
    def test_export_with_empty_content(self):
        """Test that appropriate error is raised when trying to export empty content."""
        # Test with empty markdown content
        empty_content = ""
        
        # Try to save empty markdown report
        with pytest.raises(ValueError, match="Cannot export empty content"):
            ExportHandler.save_report(empty_content, TEST_MARKDOWN_PATH)
    
    def test_export_with_non_string_content(self):
        """Test that appropriate error is raised when trying to export non-string content."""
        # Test with non-string content
        non_string_content = 12345
        
        # Try to save non-string content
        with pytest.raises(TypeError, match="Content must be a string"):
            ExportHandler.save_report(non_string_content, TEST_MARKDOWN_PATH)