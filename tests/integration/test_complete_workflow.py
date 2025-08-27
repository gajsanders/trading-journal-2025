"""
Comprehensive integration test for the complete Trading Journal workflow.

This test exercises the entire workflow from data input through report generation,
verifying that all components work together correctly. It tests the complete
pipeline: CSV processing, trade analysis, LLM insights generation, chart creation,
report assembly, and export functionality.
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the main controller and related components
from src.app.main_controller import MainController
from src.reports.report_assembler import ReportAssembler
from src.charts.chart_generator import ChartGenerator
from src.analysis.insight_generator import InsightGenerator
from src.processors.csv_processor import CSVProcessor
from src.models.trade import Trade

class TestCompleteTradingJournalWorkflow:
    """Integration tests for the complete Trading Journal workflow."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Set up test environment and clean up after each test."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp(prefix="trading_journal_test_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Create a sample CSV file with valid trades
        self.sample_csv_path = os.path.join(self.test_dir, "sample_trades.csv")
        self._create_sample_csv()

        # Create a temporary output directory
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)

        # Create a temporary data directory
        self.data_dir = os.path.join(self.test_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)

        # Reset any state that might affect tests
        self.controller = MainController()

        yield

        # Clean up after tests
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _create_sample_csv(self):
        """Create a sample CSV file with valid trades for testing."""
        csv_content = """Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity
AAPL,2.5,2024-07-01 09:30,123,Buy call,2024-07-19,150.0,Call,BTO,1
MSFT,1.8,2024-07-01 10:00,456,Buy put,2024-07-19,300.0,Put,BTO,2
GOOG,3.2,2024-07-01 11:00,789,Buy call,2024-07-19,2000.0,Call,BTO,1
TSLA,4.1,2024-07-01 12:00,1011,Buy put,2024-07-19,250.0,Put,BTO,3
AMZN,2.8,2024-07-01 13:00,1213,Buy call,2024-07-19,3000.0,Call,BTO,1"""

        with open(self.sample_csv_path, 'w') as f:
            f.write(csv_content)

    def test_complete_workflow_success(self):
        """Test the complete workflow with valid data."""
        # Arrange
        controller = MainController()

        # Act
        success = controller.process_csv(self.sample_csv_path)

        # Assert
        assert success is True
        assert controller.get_error() is None
        assert len(controller.trades) == 5

        # Test trade analysis
        analysis_success = controller.analyze_trades()
        assert analysis_success is True
        assert controller.get_error() is None
        assert controller.metrics is not None
        assert len(controller.metrics) > 0

        # Test LLM insights generation
        llm_success = controller.generate_llm_insights()
        assert llm_success is True
        assert controller.get_error() is None
        assert controller.insights is not None
        assert len(controller.insights) > 0

        # Test chart generation
        chart_success = controller.generate_charts()
        assert chart_success is True
        assert controller.get_error() is None
        assert controller.charts is not None
        assert len(controller.charts) > 0

        # Test report assembly
        report_success = controller.assemble_report()
        assert report_success is True
        assert controller.get_error() is None
        assert controller.report_content is not None
        assert len(controller.report_content) > 0

        # Test report export
        export_link = controller.export_report()
        assert export_link is not None
        assert "download_link" in export_link

        # Verify the report file was created
        report_file = os.path.join(self.output_dir, "trading_journal_report.md")
        assert os.path.exists(report_file)

        # Verify the report contains expected content
        with open(report_file, 'r') as f:
            report_content = f.read()

        assert "## Key Metrics Overview" in report_content
        assert "Total Trades: 5" in report_content
        assert "Win Rate: " in report_content
        assert "PnL: " in report_content
        assert "Key Insights" in report_content
        assert "Action Items" in report_content

    def test_workflow_with_missing_data(self):
        """Test workflow with missing data to verify error handling."""
        # Arrange
        controller = MainController()

        # Create a CSV with missing required columns
        invalid_csv_path = os.path.join(self.test_dir, "invalid_trades.csv")
        invalid_csv_content = """Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side
AAPL,2.5,2024-07-01 09:30,123,Buy call,2024-07-19,150.0,Call,BTO"""

        with open(invalid_csv_path, 'w') as f:
            f.write(invalid_csv_content)

        # Act
        success = controller.process_csv(invalid_csv_path)

        # Assert
        assert success is False
        assert controller.get_error() is not None
        assert "missing required columns" in controller.get_error().lower()
        assert controller.trades == []

        # Verify no analysis was performed
        assert controller.metrics is None
        assert controller.insights is None
        assert controller.charts is None
        assert controller.report_content is None

    def test_workflow_with_invalid_data(self):
        """Test workflow with invalid data to verify error handling."""
        # Arrange
        controller = MainController()

        # Create a CSV with invalid data
        invalid_csv_path = os.path.join(self.test_dir, "invalid_data_trades.csv")
        invalid_csv_content = """Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity
AAPL,invalid_price,2024-07-01 09:30,123,Buy call,2024-07-19,150.0,Call,BTO,1
MSFT,1.8,2024-07-01 10:00,456,Buy put,2024-07-19,300.0,Put,BTO,2"""

        with open(invalid_csv_path, 'w') as f:
            f.write(invalid_csv_content)

        # Act
        success = controller.process_csv(invalid_csv_path)

        # Assert
        assert success is False
        assert controller.get_error() is not None
        assert "invalid data" in controller.get_error().lower()
        assert controller.trades == []

        # Verify no analysis was performed
        assert controller.metrics is None
        assert controller.insights is None
        assert controller.charts is None
        assert controller.report_content is None

    def test_workflow_with_empty_csv(self):
        """Test workflow with empty CSV to verify error handling."""
        # Arrange
        controller = MainController()

        # Create an empty CSV
        empty_csv_path = os.path.join(self.test_dir, "empty_trades.csv")
        with open(empty_csv_path, 'w') as f:
            f.write("")

        # Act
        success = controller.process_csv(empty_csv_path)

        # Assert
        assert success is False
        assert controller.get_error() is not None
        assert "empty file" in controller.get_error().lower()
        assert controller.trades == []

        # Verify no analysis was performed
        assert controller.metrics is None
        assert controller.insights is None
        assert controller.charts is None
        assert controller.report_content is None

    def test_workflow_with_large_dataset(self):
        """Test workflow with a large dataset to verify performance."""
        # Arrange
        controller = MainController()

        # Create a large CSV with many trades
        large_csv_path = os.path.join(self.test_dir, "large_trades.csv")

        # Generate a large dataset with 100 trades
        trades = []
        for i in range(100):
            trades.append(f"""AAPL,{2.5 + i*0.1},2024-07-01 09:30,{1000+i},Buy call,2024-07-19,{150 + i},Call,BTO,1""")

        csv_content = """Symbol,Price,Time,Order #,Description,Expiry,Strike,OptionType,Side,Quantity\n"""
        csv_content += "\n".join(trades)

        with open(large_csv_path, 'w') as f:
            f.write(csv_content)

        # Act
        success = controller.process_csv(large_csv_path)

        # Assert
        assert success is True
        assert controller.get_error() is None
        assert len(controller.trades) == 100

        # Test analysis with large dataset
        analysis_success = controller.analyze_trades()
        assert analysis_success is True
        assert controller.get_error() is None
        assert controller.metrics is not None

        # Test LLM insights generation
        llm_success = controller.generate_llm_insights()
        assert llm_success is True
        assert controller.get_error() is None
        assert controller.insights is not None

        # Test chart generation
        chart_success = controller.generate_charts()
        assert chart_success is True
        assert controller.get_error() is None
        assert controller.charts is not None

        # Test report assembly
        report_success = controller.assemble_report()
        assert report_success is True
        assert controller.get_error() is None
        assert controller.report_content is not None

        # Test report export
        export_link = controller.export_report()
        assert export_link is not None
        assert "download_link" in export_link

        # Verify the report file was created
        report_file = os.path.join(self.output_dir, "trading_journal_report.md")
        assert os.path.exists(report_file)

        # Verify the report contains expected content
        with open(report_file, 'r') as f:
            report_content = f.read()

        assert "## Key Metrics Overview" in report_content
        assert "Total Trades: 100" in report_content
        assert "Win Rate: " in report_content
        assert "PnL: " in report_content
        assert "Key Insights" in report_content
        assert "Action Items" in report_content

    def test_workflow_with_custom_configuration(self):
        """Test workflow with custom configuration to verify flexibility."""
        # Arrange
        controller = MainController()

        # Set custom configuration
        controller.config = {
            "output_dir": self.output_dir,
            "data_dir": self.data_dir,
            "report_template": "custom_template.md",
            "enable_llm_analysis": True,
            "enable_chart_generation": True,
            "max_trades_per_report": 50
        }

        # Process the sample CSV
        success = controller.process_csv(self.sample_csv_path)

        # Assert
        assert success is True
        assert controller.get_error() is None
        assert len(controller.trades) == 5

        # Test analysis
        analysis_success = controller.analyze_trades()
        assert analysis_success is True
        assert controller.get_error() is None

        # Test LLM insights
        llm_success = controller.generate_llm_insights()
        assert llm_success is True
        assert controller.get_error() is None

        # Test chart generation
        chart_success = controller.generate_charts()
        assert chart_success is True
        assert controller.get_error() is None

        # Test report assembly
        report_success = controller.assemble_report()
        assert report_success is True
        assert controller.get_error() is None

        # Test export
        export_link = controller.export_report()
        assert export_link is not None
        assert "download_link" in export_link

        # Verify the report file was created
        report_file = os.path.join(self.output_dir, "trading_journal_report.md")
        assert os.path.exists(report_file)

        # Verify the report contains expected content
        with open(report_file, 'r') as f:
            report_content = f.read()

        assert "## Key Metrics Overview" in report_content
        assert "Total Trades: 5" in report_content
        assert "Win Rate: " in report_content
        assert "PnL: " in report_content
        assert "Key Insights" in report_content
        assert "Action Items" in report_content

    def test_workflow_with_mocked_components(self):
        """Test workflow with mocked components to verify integration."""
        # Arrange
        controller = MainController()

        # Mock all components to verify they are called correctly
        with patch.object(CSVProcessor, 'load_csv') as mock_load_csv, \
             patch.object(CSVProcessor, 'to_trades') as mock_to_trades, \
             patch.object(InsightGenerator, 'generate_insights') as mock_generate_insights, \
             patch.object(ChartGenerator, 'generate_charts') as mock_generate_charts, \
             patch.object(ReportAssembler, 'assemble_report') as mock_assemble_report, \
             patch.object(MainController, 'export_report') as mock_export_report:

            # Set up mocks to return valid data
            mock_load_csv.return_value = MagicMock()
            mock_to_trades.return_value = [MagicMock(spec=Trade) for _ in range(5)]
            mock_generate_insights.return_value = ["Insight 1", "Insight 2"]
            mock_generate_charts.return_value = ["chart1.png", "chart2.png"]
            mock_assemble_report.return_value = "Mocked report content"
            mock_export_report.return_value = "download_link"

            # Act
            success = controller.process_csv(self.sample_csv_path)

            # Assert
            assert success is True
            assert controller.get_error() is None

            # Verify all components were called
            mock_load_csv.assert_called_once()
            mock_to_trades.assert_called_once()
            mock_generate_insights.assert_called_once()
            mock_generate_charts.assert_called_once()
            mock_assemble_report.assert_called_once()
            mock_export_report.assert_called_once()

            # Verify the controller state was updated
            assert len(controller.trades) == 5
            assert controller.insights == ["Insight 1", "Insight 2"]
            assert controller.charts == ["chart1.png", "chart2.png"]
            assert controller.report_content == "Mocked report content"

    def test_workflow_with_error_recovery(self):
        """Test workflow with error recovery to verify resilience."""
        # Arrange
        controller = MainController()

        # Set up error recovery
        controller.config = {
            "error_recovery": True,
            "max_retries": 3,
            "retry_delay": 0.1
        }

        # Process the sample CSV
        success = controller.process_csv(self.sample_csv_path)

        # Assert
        assert success is True
        assert controller.get_error() is None
        assert len(controller.trades) == 5

        # Test analysis with error recovery
        analysis_success = controller.analyze_trades()
        assert analysis_success is True
        assert controller.get_error() is None

        # Test LLM insights with error recovery
        llm_success = controller.generate_llm_insights()
        assert llm_success is True
        assert controller.get_error() is None

        # Test chart generation with error recovery
        chart_success = controller.generate_charts()
        assert chart_success is True
        assert controller.get_error() is None

        # Test report assembly with error recovery
        report_success = controller.assemble_report()
        assert report_success is True
        assert controller.get_error() is None

        # Test export with error recovery
        export_link = controller.export_report()
        assert export_link is not None
        assert "download_link" in export_link

        # Verify the report file was created
        report_file = os.path.join(self.output_dir, "trading_journal_report.md")
        assert os.path.exists(report_file)

        # Verify the report contains expected content
        with open(report_file, 'r') as f:
            report_content = f.read()

        assert "## Key Metrics Overview" in report_content
        assert "Total Trades: 5" in report_content
        assert "Win Rate: " in report_content
        assert "PnL: " in report_content
        assert "Key Insights" in report_content
        assert "Action Items" in report_content
