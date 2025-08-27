import os
import tempfile
from unittest.mock import patch
import pytest
from src.app.streamlit_app import main
import streamlit as st
from src.config import Config

def test_streamlit_app_with_invalid_config(monkeypatch):
    """Test that Streamlit app shows error message with invalid configuration."""
    # Mock st.error to capture calls
    error_calls = []
    def mock_error(message):
        error_calls.append(message)
    
    monkeypatch.setattr(st, 'error', mock_error)
    
    # Mock st.set_page_config and st.title to avoid Streamlit errors in test
    monkeypatch.setattr(st, 'set_page_config', lambda **kwargs: None)
    monkeypatch.setattr(st, 'title', lambda title: None)
    
    with patch.dict(os.environ, {}, clear=True):
        # Remove WORKSPACE_ROOT to simulate invalid config
        if 'WORKSPACE_ROOT' in os.environ:
            del os.environ['WORKSPACE_ROOT']
        
        # Call main function
        main()
        
        # Verify error was shown
        assert len(error_calls) > 0
        assert "Configuration Error" in error_calls[0]

def test_streamlit_app_with_valid_config(monkeypatch):
    """Test that Streamlit app initializes correctly with valid configuration."""
    # Mock st.set_page_config and st.title to avoid Streamlit errors in test
    monkeypatch.setattr(st, 'set_page_config', lambda **kwargs: None)
    monkeypatch.setattr(st, 'title', lambda title: None)
    
    # Mock UI components to avoid Streamlit errors in test
    monkeypatch.setattr('src.app.streamlit_app.file_upload_component', lambda: None)
    monkeypatch.setattr('src.app.streamlit_app.section_header', lambda header: None)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        with patch.dict(os.environ, {'WORKSPACE_ROOT': tmp_dir}):
            # Should not raise any exceptions
            main()