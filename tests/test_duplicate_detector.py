import pandas as pd
import pytest
from src.processors.duplicate_detector import DuplicateDetector

def test_find_duplicates_sample():
    df = pd.read_csv("tests/sample_duplicates.csv")
    detector = DuplicateDetector(df)
    dupes = detector.find_duplicates()
    assert not dupes.empty
    assert all(dupes["Order # Clean"] == "2001")
    assert len(dupes) == 2

def test_duplicate_summary_sample():
    df = pd.read_csv("tests/sample_duplicates.csv")
    detector = DuplicateDetector(df)
    summary = detector.duplicate_summary()
    assert summary["num_duplicate_order_numbers"] == 1
    assert summary["total_duplicate_records"] == 2
    assert "2001" in summary["duplicate_order_numbers"]

def test_structured_results_sample():
    df = pd.read_csv("tests/sample_duplicates.csv")
    detector = DuplicateDetector(df)
    results = detector.structured_results()
    assert "summary" in results
    assert "duplicate_records" in results
    assert isinstance(results["duplicate_records"], list)
    assert results["summary"]["num_duplicate_order_numbers"] == 1

def test_no_duplicates_sample():
    df = pd.read_csv("tests/sample_valid_trades.csv")
    detector = DuplicateDetector(df)
    dupes = detector.find_duplicates()
    assert dupes.empty
    summary = detector.duplicate_summary()
    assert summary["num_duplicate_order_numbers"] == 0
    assert summary["total_duplicate_records"] == 0
    assert summary["duplicate_order_numbers"] == []

def test_with_real_tastytrade_csv():
    df = pd.read_csv("tastytrade_activity_250716.csv")
    detector = DuplicateDetector(df)
    # Should not raise or error
    summary = detector.duplicate_summary()
    assert isinstance(summary, dict)
    assert "num_duplicate_order_numbers" in summary 

def sample_df():
    return pd.DataFrame([
        {"Order #": "123", "Symbol": "AAPL", "Price": 1.0},
        {"Order #": "124", "Symbol": "AAPL", "Price": 2.0},
        {"Order #": "123", "Symbol": "AAPL", "Price": 1.1},
        {"Order #": "125", "Symbol": "MSFT", "Price": 3.0},
        {"Order #": "124", "Symbol": "AAPL", "Price": 2.1},
    ])

def test_structured_results():
    df = sample_df()
    detector = DuplicateDetector(df)
    results = detector.structured_results()
    summary = results["summary"]
    records = results["duplicate_records"]
    # There should be 2 duplicate order numbers: 123 and 124
    assert summary["num_duplicate_order_numbers"] == 2
    assert summary["total_duplicate_records"] == 4
    assert set(summary["duplicate_order_numbers"]) == {"123", "124"}
    # There should be 4 duplicate records
    assert isinstance(records, list)
    assert len(records) == 4
    # Each record should have Order # in 123 or 124
    for rec in records:
        assert rec["Order #"] in ("123", "124")
        assert "Symbol" in rec and "Price" in rec

def test_no_duplicates():
    df = pd.DataFrame([
        {"Order #": "1", "Symbol": "AAPL"},
        {"Order #": "2", "Symbol": "MSFT"},
    ])
    detector = DuplicateDetector(df)
    results = detector.structured_results()
    assert results["summary"]["num_duplicate_order_numbers"] == 0
    assert results["summary"]["total_duplicate_records"] == 0
    assert results["duplicate_records"] == [] 

def test_mock_duplicate_handling(monkeypatch):
    # Simulate DataFrame.duplicated to mark only first two rows as duplicates
    df = pd.DataFrame([
        {"Order #": "1", "Symbol": "AAPL"},
        {"Order #": "1", "Symbol": "AAPL"},
        {"Order #": "2", "Symbol": "MSFT"},
    ])
    orig_duplicated = pd.DataFrame.duplicated
    monkeypatch.setattr(pd.DataFrame, "duplicated", lambda self, *a, **kw: pd.Series([True, True, False], index=self.index))
    detector = DuplicateDetector(df)
    results = detector.structured_results()
    assert results["summary"]["num_duplicate_order_numbers"] == 1
    assert results["summary"]["total_duplicate_records"] == 2
    assert results["duplicate_records"][0]["Order #"] == "1"
    # Restore original method to avoid side effects
    pd.DataFrame.duplicated = orig_duplicated 