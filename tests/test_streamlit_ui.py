from src.app import ui_components
from unittest.mock import patch, MagicMock
import os
import pytest
from streamlit.testing.v1 import AppTest

def test_section_header():
    with patch('streamlit.markdown') as mock_md:
        ui_components.section_header("Test Header")
        mock_md.assert_called_once()
        assert "Test Header" in mock_md.call_args[0][0]

def test_error_message_component():
    with patch('streamlit.error') as mock_err:
        ui_components.error_message_component("Error!")
        mock_err.assert_called_once_with("Error!")

def test_progress_component():
    with patch('streamlit.progress') as mock_prog, patch('streamlit.write') as mock_write:
        ui_components.progress_component(0.5, "Processing...")
        mock_prog.assert_called_once_with(0.5)
        mock_write.assert_called_once_with("Processing...")

def test_file_upload_component():
    with patch('streamlit.file_uploader', return_value=None) as mock_uploader:
        result = ui_components.file_upload_component()
        mock_uploader.assert_called_once()
        assert result is None
    with patch('streamlit.file_uploader', return_value="dummy.csv") as mock_uploader:
        result = ui_components.file_upload_component()
        assert result == "dummy.csv"

# --- UI tests up to file upload point ---
def test_streamlit_app_pre_upload_ui():
    """
    Test that the Streamlit app renders the upload section and pre-upload UI state correctly.
    File upload simulation is not supported by AppTest; see README for details.
    """
    at = AppTest.from_file("src/app/streamlit_app.py").run()
    # Just check that the app runs without errors
    assert not at.exception

# --- Note: File upload simulation and full workflow UI integration tests are not possible with AppTest as of July 2024. See README for details. --- 