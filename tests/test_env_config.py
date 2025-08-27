import os
import tempfile
from pathlib import Path
from unittest.mock import patch
import pytest
from src.config import Config

def test_workspace_root_unset():
    """Test that application correctly flags error when WORKSPACE_ROOT is unset."""
    with patch.dict(os.environ, {}, clear=True):
        # Remove WORKSPACE_ROOT if it exists
        if 'WORKSPACE_ROOT' in os.environ:
            del os.environ['WORKSPACE_ROOT']
        
        is_valid, error_message = Config.validate()
        assert not is_valid
        assert "WORKSPACE_ROOT environment variable is not set" in error_message

def test_workspace_root_empty():
    """Test that application correctly flags error when WORKSPACE_ROOT is empty."""
    with patch.dict(os.environ, {'WORKSPACE_ROOT': ''}):
        is_valid, error_message = Config.validate()
        assert not is_valid
        assert "WORKSPACE_ROOT environment variable is not set" in error_message

def test_workspace_root_nonexistent():
    """Test that application correctly flags error when WORKSPACE_ROOT points to nonexistent path."""
    nonexistent_path = "/this/path/does/not/exist/12345"
    with patch.dict(os.environ, {'WORKSPACE_ROOT': nonexistent_path}):
        is_valid, error_message = Config.validate()
        assert not is_valid
        assert f"WORKSPACE_ROOT path '{nonexistent_path}' does not exist" in error_message

def test_workspace_root_is_file():
    """Test that application correctly flags error when WORKSPACE_ROOT points to a file."""
    with tempfile.NamedTemporaryFile() as tmp_file:
        with patch.dict(os.environ, {'WORKSPACE_ROOT': tmp_file.name}):
            is_valid, error_message = Config.validate()
            assert not is_valid
            assert f"WORKSPACE_ROOT path '{tmp_file.name}' is not a directory" in error_message

def test_workspace_root_valid():
    """Test that application validates correctly when WORKSPACE_ROOT is properly set."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        with patch.dict(os.environ, {'WORKSPACE_ROOT': tmp_dir}):
            is_valid, error_message = Config.validate()
            assert is_valid
            assert error_message == ""

def test_config_values():
    """Test that Config class correctly retrieves environment variables."""
    test_api_key = "test-api-key-123"
    test_log_level = "DEBUG"
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        with patch.dict(os.environ, {
            'WORKSPACE_ROOT': tmp_dir,
            'OPENAI_API_KEY': test_api_key,
            'LOG_LEVEL': test_log_level
        }):
            assert Config.get_workspace_root() == tmp_dir
            assert Config.get_openai_api_key() == test_api_key
            assert Config.get_log_level() == test_log_level

def test_config_defaults():
    """Test that Config class uses appropriate defaults."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        with patch.dict(os.environ, {'WORKSPACE_ROOT': tmp_dir}, clear=True):
            # Remove other env vars to test defaults
            env_vars_to_remove = ['OPENAI_API_KEY', 'LOG_LEVEL']
            for var in env_vars_to_remove:
                if var in os.environ:
                    del os.environ[var]
            
            assert Config.get_openai_api_key() == ""
            assert Config.get_log_level() == "INFO"