import os
import tempfile
from unittest.mock import patch
import pytest
from src.config import Config
from src.app.main_controller import MainController

def test_application_startup_with_invalid_config():
    """Test that application startup correctly handles invalid configuration."""
    with patch.dict(os.environ, {}, clear=True):
        # Remove WORKSPACE_ROOT to simulate invalid config
        if 'WORKSPACE_ROOT' in os.environ:
            del os.environ['WORKSPACE_ROOT']
        
        # Validate config
        is_valid, error_message = Config.validate()
        assert not is_valid
        assert "WORKSPACE_ROOT environment variable is not set" in error_message

def test_application_startup_with_valid_config():
    """Test that application startup works with valid configuration."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        with patch.dict(os.environ, {'WORKSPACE_ROOT': tmp_dir}):
            # Validate config
            is_valid, error_message = Config.validate()
            assert is_valid
            assert error_message == ""
            
            # Initialize controller (should work with valid config)
            controller = MainController()
            assert controller is not None