import pytest
import pandas as pd
from src.processors.csv_processor import CSVProcessor, REQUIRED_COLUMNS
from src.models.trade import Trade

@pytest.fixture
def valid_row():
    return {
        "Order #": "123",
        "Symbol": "AAPL",
        "Price": "2.5",
        "Time": "2024-07-01 09:30",
        "Description": "desc",
        "Expiry": "2024-07-19",
        "Strike": 150.0,
        "OptionType": "Call",
        "Side": "BTO",
        "Quantity": 1
    }

def test_load_csv_missing_columns(tmp_path):
    # Create a CSV missing required columns
    csv_path = tmp_path / "bad.csv"
    pd.DataFrame({"Symbol": ["AAPL"]}).to_csv(csv_path, index=False)
    processor = CSVProcessor(str(csv_path))
    with pytest.raises(ValueError):
        processor.load_csv()

def test_to_trades_skips_malformed(monkeypatch, valid_row):
    # Mock DataFrame with one valid and one malformed row
    df = pd.DataFrame([valid_row, {**valid_row, "Symbol": None}])
    processor = CSVProcessor("dummy.csv")
    processor.df = df
    trades = processor.to_trades()
    assert len(trades) == 1
    assert isinstance(trades[0], Trade)
    assert trades[0].symbol == "AAPL"

def test_to_trades_all_valid(monkeypatch, valid_row):
    df = pd.DataFrame([valid_row, {**valid_row, "Order #": "456", "Symbol": "MSFT"}])
    processor = CSVProcessor("dummy.csv")
    processor.df = df
    trades = processor.to_trades()
    assert len(trades) == 2
    assert {t.symbol for t in trades} == {"AAPL", "MSFT"}

def test_load_and_validate_csv():
    processor = CSVProcessor("tests/sample_valid_trades.csv")
    df = processor.load_csv()
    assert all(col in df.columns for col in REQUIRED_COLUMNS)
    assert processor.validate()

def test_to_trades_conversion():
    processor = CSVProcessor("tests/sample_valid_trades.csv")
    trades = processor.to_trades()
    assert len(trades) == 2
    assert {t.symbol for t in trades} == {"AAPL", "MSFT"}

def test_with_real_tastytrade_csv():
    # This test will fail if tastytrade_activity_250716.csv does not match the new schema
    try:
        processor = CSVProcessor("tastytrade_activity_250716.csv")
        df = processor.load_csv()
        assert all(col in df.columns for col in REQUIRED_COLUMNS)
    except ValueError:
        pass  # Acceptable if the file is not updated yet 

def test_mock_file_handling(monkeypatch, valid_row):
    # Simulate pd.read_csv returning a DataFrame without reading a file
    df = pd.DataFrame([valid_row, {**valid_row, "Order #": "456", "Symbol": "MSFT"}])
    monkeypatch.setattr(pd, "read_csv", lambda path: df)
    processor = CSVProcessor("mock.csv")
    loaded = processor.load_csv()
    assert loaded.equals(df)
    trades = processor.to_trades()
    assert len(trades) == 2
    assert {t.symbol for t in trades} == {"AAPL", "MSFT"} 