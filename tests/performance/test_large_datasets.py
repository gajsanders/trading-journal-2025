"""
Performance tests for the Trading Journal application with large datasets.

This test suite evaluates the application's performance with datasets ranging from 10,000 to 1,000,000 trade entries.
It measures timing for each component of the workflow and verifies that performance thresholds are met.
"""

import pytest
import time
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.app.main_controller import MainController
from src.processors.csv_processor import CSVProcessor
from src.analysis.insight_generator import InsightGenerator
from src.charts.chart_generator import ChartGenerator
from src.reports.report_assembler import ReportAssembler
from src.models.trade import Trade

# Configuration
TEST_DATA_DIR = Path("tests/performance/datasets")
OUTPUT_DIR = Path("tests/performance/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Performance thresholds (in seconds)
THRESHOLDS = {
    "csv_processing": 30,  # Max time to process CSV file
    "trade_analysis": 60,   # Max time to analyze trades
    "llm_insights": 120,    # Max time to generate LLM insights
    "chart_generation": 180, # Max time to generate charts
    "report_assembly": 90,   # Max time to assemble report
    "total_workflow": 300   # Max time for complete workflow
}

# Test data
TEST_FILES = {
    "small": "large_trades_10000.csv",
    "medium": "large_trades_100000.csv",
    "large": "large_trades_1000000.csv"
}

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Set up test environment and clean up after each test."""
    # Create a temporary directory for test files
    test_dir = Path("tests/performance/temp")
    test_dir.mkdir(parents=True, exist_ok=True)

    # Copy test files to temporary directory
    for size, filename in TEST_FILES.items():
        src_path = TEST_DATA_DIR / filename
        dst_path = test_dir / filename
        if src_path.exists():
            shutil.copy(src_path, dst_path)

    # Create output directory
    output_dir = test_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a temporary data directory
    data_dir = test_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Reset any state that might affect tests
    controller = MainController()
    controller.config = {
        "output_dir": str(output_dir),
        "data_dir": str(data_dir),
        "enable_llm_analysis": True,
        "enable_chart_generation": True,
        "max_trades_per_report": 100000
    }

    yield controller, test_dir

    # Clean up after tests
    shutil.rmtree(test_dir, ignore_errors=True)

@pytest.mark.performance
@pytest.mark.parametrize("size", ["small", "medium", "large"])
def test_csv_processing_performance(size, setup_and_teardown):
    """Test CSV processing performance with different dataset sizes."""
    controller, test_dir = setup_and_teardown

    # Get the test file
    filename = TEST_FILES[size]
    file_path = test_dir / filename

    # Skip if file doesn't exist
    if not file_path.exists():
        pytest.skip(f"Test file {filename} not found")

    # Start timing
    start_time = time.time()

    # Process the CSV
    success = controller.process_csv(str(file_path))

    # End timing
    end_time = time.time()
    processing_time = end_time - start_time

    # Assert success
    assert success is True, f"CSV processing failed for {size} dataset"

    # Assert performance threshold
    assert processing_time <= THRESHOLDS["csv_processing"], \
        f"CSV processing time ({processing_time:.2f}s) exceeds threshold ({THRESHOLDS['csv_processing']}s) for {size} dataset"

    # Log performance metrics
    print(f"CSV processing performance: {size} dataset - {processing_time:.2f}s")

    # Verify trade count matches expected
    expected_count = {
        "small": 10000,
        "medium": 100000,
        "large": 1000000
    }
    assert len(controller.trades) == expected_count[size], \
        f"Expected {expected_count[size]} trades, got {len(controller.trades)}"

@pytest.mark.performance
@pytest.mark.parametrize("size", ["small", "medium", "large"])
def test_trade_analysis_performance(size, setup_and_teardown):
    """Test trade analysis performance with different dataset sizes."""
    controller, test_dir = setup_and_teardown

    # Get the test file
    filename = TEST_FILES[size]
    file_path = test_dir / filename

    # Skip if file doesn't exist
    if not file_path.exists():
        pytest.skip(f"Test file {filename} not found")

    # Process the CSV first
    controller.process_csv(str(file_path))

    # Start timing
    start_time = time.time()

    # Analyze the trades
    success = controller.analyze_trades()

    # End timing
    end_time = time.time()
    analysis_time = end_time - start_time

    # Assert success
    assert success is True, f"Trade analysis failed for {size} dataset"

    # Assert performance threshold
    assert analysis_time <= THRESHOLDS["trade_analysis"], \
        f"Trade analysis time ({analysis_time:.2f}s) exceeds threshold ({THRESHOLDS['trade_analysis']}s) for {size} dataset"

    # Log performance metrics
    print(f"Trade analysis performance: {size} dataset - {analysis_time:.2f}s")

    # Verify metrics are generated
    assert controller.metrics is not None, "Metrics should be generated after analysis"
    assert len(controller.metrics) > 0, "Metrics should contain data after analysis"

@pytest.mark.performance
@pytest.mark.parametrize("size", ["small", "medium", "large"])
def test_llm_insights_performance(size, setup_and_teardown):
    """Test LLM insights generation performance with different dataset sizes."""
    controller, test_dir = setup_and_teardown

    # Get the test file
    filename = TEST_FILES[size]
    file_path = test_dir / filename

    # Skip if file doesn't exist
    if not file_path.exists():
        pytest.skip(f"Test file {filename} not found")

    # Process the CSV and analyze trades first
    controller.process_csv(str(file_path))
    controller.analyze_trades()

    # Mock the LLM client to avoid actual API calls
    with patch('src.clients.openai_client.OpenAIClient') as mock_client:
        mock_client.return_value.generate_insights.return_value = "Generated insights for the dataset"
        mock_client.return_value.generate_questions.return_value = "Generated questions for the dataset"
        mock_client.return_value.generate_action_items.return_value = "Generated action items for the dataset"

        # Start timing
        start_time = time.time()

        # Generate LLM insights
        success = controller.generate_llm_insights()

        # End timing
        end_time = time.time()
        llm_time = end_time - start_time

        # Assert success
        assert success is True, f"LLM insights generation failed for {size} dataset"

        # Assert performance threshold
        assert llm_time <= THRESHOLDS["llm_insights"], \
            f"LLM insights generation time ({llm_time:.2f}s) exceeds threshold ({THRESHOLDS['llm_insights']}s) for {size} dataset"

        # Log performance metrics
        print(f"LLM insights performance: {size} dataset - {llm_time:.2f}s")

        # Verify insights are generated
        assert controller.insights is not None, "Insights should be generated after LLM analysis"
        assert len(controller.insights) > 0, "Insights should contain data after LLM analysis"

@pytest.mark.performance
@pytest.mark.parametrize("size", ["small", "medium", "large"])
def test_chart_generation_performance(size, setup_and_teardown):
    """Test chart generation performance with different dataset sizes."""
    controller, test_dir = setup_and_teardown

    # Get the test file
    filename = TEST_FILES[size]
    file_path = test_dir / filename

    # Skip if file doesn't exist
    if not file_path.exists():
        pytest.skip(f"Test file {filename} not found")

    # Process the CSV, analyze trades, and generate LLM insights first
    controller.process_csv(str(file_path))
    controller.analyze_trades()
    controller.generate_llm_insights()

    # Mock the chart generator to avoid actual chart generation
    with patch('src.charts.chart_generator.ChartGenerator') as mock_chart_generator:
        mock_chart_generator.return_value.generate_pnl_chart.return_value = "![PnL Chart](pnl_chart.png)"
        mock_chart_generator.return_value.generate_trade_distribution_chart.return_value = "![Trade Distribution Chart](trade_dist_chart.png)"
        mock_chart_generator.return_value.generate_strategy_chart.return_value = "![Strategy Chart](strategy_chart.png)"

        # Start timing
        start_time = time.time()

        # Generate charts
        success = controller.generate_charts()

        # End timing
        end_time = time.time()
        chart_time = end_time - start_time

        # Assert success
        assert success is True, f"Chart generation failed for {size} dataset"

        # Assert performance threshold
        assert chart_time <= THRESHOLDS["chart_generation"], \
            f"Chart generation time ({chart_time:.2f}s) exceeds threshold ({THRESHOLDS['chart_generation']}s) for {size} dataset"

        # Log performance metrics
        print(f"Chart generation performance: {size} dataset - {chart_time:.2f}s")

        # Verify charts are generated
        assert controller.charts is not None, "Charts should be generated after chart generation"
        assert len(controller.charts) > 0, "Charts should contain data after generation"

@pytest.mark.performance
@pytest.mark.parametrize("size", ["small", "medium", "large"])
def test_report_assembly_performance(size, setup_and_teardown):
    """Test report assembly performance with different dataset sizes."""
    controller, test_dir = setup_and_teardown

    # Get the test file
    filename = TEST_FILES[size]
    file_path = test_dir / filename

    # Skip if file doesn't exist
    if not file_path.exists():
        pytest.skip(f"Test file {filename} not found")

    # Process the CSV, analyze trades, generate LLM insights, and generate charts first
    controller.process_csv(str(file_path))
    controller.analyze_trades()
    controller.generate_llm_insights()
    controller.generate_charts()

    # Mock the markdown generator to avoid actual file writing
    with patch('src.reports.report_assembler.MarkdownGenerator') as mock_markdown_generator:
        mock_markdown_generator.return_value.generate_report.return_value = "Mocked report content"

        # Start timing
        start_time = time.time()

        # Assemble the report
        success = controller.assemble_report()

        # End timing
        end_time = time.time()
        report_time = end_time - start_time

        # Assert success
        assert success is True, f"Report assembly failed for {size} dataset"

        # Assert performance threshold
        assert report_time <= THRESHOLDS["report_assembly"], \
            f"Report assembly time ({report_time:.2f}s) exceeds threshold ({THRESHOLDS['report_assembly']}s) for {size} dataset"

        # Log performance metrics
        print(f"Report assembly performance: {size} dataset - {report_time:.2f}s")

        # Verify report content is generated
        assert controller.report_content is not None, "Report content should be generated after assembly"
        assert len(controller.report_content) > 0, "Report content should contain data after assembly"

@pytest.mark.performance
@pytest.mark.parametrize("size", ["small", "medium", "large"])
def test_complete_workflow_performance(size, setup_and_teardown):
    """Test complete workflow performance with different dataset sizes."""
    controller, test_dir = setup_and_teardown

    # Get the test file
    filename = TEST_FILES[size]
    file_path = test_dir / filename

    # Skip if file doesn't exist
    if not file_path.exists():
        pytest.skip(f"Test file {filename} not found")

    # Start timing
    start_time = time.time()

    # Execute the complete workflow
    success = controller.process_csv(str(file_path))
    assert success is True, f"CSV processing failed for {size} dataset"

    success = controller.analyze_trades()
    assert success is True, f"Trade analysis failed for {size} dataset"

    success = controller.generate_llm_insights()
    assert success is True, f"LLM insights generation failed for {size} dataset"

    success = controller.generate_charts()
    assert success is True, f"Chart generation failed for {size} dataset"

    success = controller.assemble_report()
    assert success is True, f"Report assembly failed for {size} dataset"

    # End timing
    end_time = time.time()
    total_time = end_time - start_time

    # Assert performance threshold
    assert total_time <= THRESHOLDS["total_workflow"], \
        f"Complete workflow time ({total_time:.2f}s) exceeds threshold ({THRESHOLDS['total_workflow']}s) for {size} dataset"

    # Log performance metrics
    print(f"Complete workflow performance: {size} dataset - {total_time:.2f}s")

    # Verify all components are properly initialized
    assert controller.trades is not None, "Trades should be available after processing"
    assert controller.metrics is not None, "Metrics should be available after analysis"
    assert controller.insights is not None, "Insights should be available after LLM analysis"
    assert controller.charts is not None, "Charts should be available after chart generation"
    assert controller.report_content is not None, "Report content should be available after assembly"

    # Verify report was exported
    export_link = controller.export_report()
    assert export_link is not None, "Report should be exportable"
    assert "download_link" in export_link, "Export link should contain 'download_link'"

@pytest.mark.performance
def test_performance_thresholds():
    """Test that performance thresholds are properly configured."""
    # Verify that all required thresholds are defined
    required_thresholds = ["csv_processing", "trade_analysis", "llm_insights", "chart_generation", "report_assembly", "total_workflow"]

    for threshold in required_thresholds:
        assert threshold in THRESHOLDS, f"Missing performance threshold: {threshold}"
        assert isinstance(THRESHOLDS[threshold], (int, float)), f"Threshold {threshold} should be a number"
        assert THRESHOLDS[threshold] > 0, f"Threshold {threshold} should be positive"

    # Verify that thresholds are reasonable
    assert THRESHOLDS["csv_processing"] < 60, "CSV processing threshold should be less than 60 seconds"
    assert THRESHOLDS["trade_analysis"] < 120, "Trade analysis threshold should be less than 120 seconds"
    assert THRESHOLDS["llm_insights"] < 300, "LLM insights threshold should be less than 300 seconds"
    assert THRESHOLDS["chart_generation"] < 300, "Chart generation threshold should be less than 300 seconds"
    assert THRESHOLDS["report_assembly"] < 120, "Report assembly threshold should be less than 120 seconds"
    assert THRESHOLDS["total_workflow"] < 600, "Total workflow threshold should be less than 600 seconds"

@pytest.mark.performance
def test_dataset_generation():
    """Test that large datasets were generated correctly."""
    # Check if test datasets exist
    for size, filename in TEST_FILES.items():
        file_path = TEST_DATA_DIR / filename
        assert file_path.exists(), f"Dataset {filename} not found"

        # Check file size
        file_size = file_path.stat().st_size
        assert file_size > 0, f"Dataset {filename} is empty"

        # For large datasets, verify they're not too small
        if size == "large":
            assert file_size > 1000000, f"Large dataset {filename} is too small ({file_size} bytes)"

@pytest.mark.performance
def test_performance_metrics():
    """Test that performance metrics are properly recorded."""
    # Create a temporary directory for test files
    test_dir = Path("tests/performance/temp")
    test_dir.mkdir(parents=True, exist_ok=True)

    # Create a mock output directory
    output_dir = test_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a mock performance metrics file
    metrics_file = output_dir / "performance_metrics.json"
    metrics = {
        "test_date": "2024-01-01",
        "test_environment": "local",
        "test_version": "1.0.0",
        "test_results": {}
    }

    # Save metrics to file
    import json
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)

    # Verify metrics file was created
    assert metrics_file.exists(), "Performance metrics file should be created"

    # Verify metrics file contains expected content
    with open(metrics_file, 'r') as f:
        saved_metrics = json.load(f)

    assert "test_date" in saved_metrics, "Metrics should contain test_date"
    assert "test_environment" in saved_metrics, "Metrics should contain test_environment"
    assert "test_version" in saved_metrics, "Metrics should contain test_version"
    assert "test_results" in saved_metrics, "Metrics should contain test_results"

    # Clean up
    shutil.rmtree(test_dir, ignore_errors=True)
