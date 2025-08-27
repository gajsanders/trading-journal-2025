import pandas as pd
from unittest.mock import patch, MagicMock
from src.app.data_handler import DataHandler
from src.app.duplicate_ui import DuplicateUI
import pytest
from src.app.data_handler import DataHandler
import shutil
import os

def test_data_handler_process_csv(tmp_path):
    # Copy the valid sample CSV to the temp path
    src = os.path.join(os.path.dirname(__file__), "sample_valid_trades.csv")
    dst = tmp_path / "test.csv"
    shutil.copy(src, dst)
    handler = DataHandler()
    result = handler.process_csv(str(dst))
    assert isinstance(result, dict)
    assert "trades" in result

def test_duplicate_ui_show_duplicates():
    df = pd.DataFrame({
        'Order # Clean': ['123', '123'],
        'Symbol': ['AAPL', 'AAPL']
    })
    with patch('streamlit.success') as mock_success, \
         patch('streamlit.warning') as mock_warning, \
         patch('streamlit.button', return_value=False), \
         patch('streamlit.checkbox', return_value=False), \
         patch('streamlit.dataframe') as mock_df, \
         patch('streamlit.info') as mock_info:
        DuplicateUI.show_duplicates(df)
        mock_warning.assert_called()
    # Test no duplicates
    empty_df = pd.DataFrame({'Order # Clean': []})
    with patch('streamlit.success') as mock_success:
        DuplicateUI.show_duplicates(empty_df)
        mock_success.assert_called() 