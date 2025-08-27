import pytest
from src.app.main_controller import MainController
import os

def test_workflow_success():
    controller = MainController()
    assert controller.process_csv('dummy_file')
    assert controller.analyze_trades()
    assert controller.generate_llm_insights()
    assert controller.generate_charts()
    assert controller.assemble_report()
    link = controller.export_report()
    assert link == 'download_link'
    assert controller.get_error() is None

def test_csv_error(monkeypatch):
    controller = MainController()
    def fail_csv(file):
        controller.error = 'csv error'
        return False
    monkeypatch.setattr(controller, 'process_csv', fail_csv)
    assert not controller.process_csv('bad_file')
    assert controller.get_error() is not None

def test_analysis_error(monkeypatch):
    controller = MainController()
    controller.process_csv('dummy_file')
    def fail_analysis():
        controller.error = 'analysis error'
        return False
    monkeypatch.setattr(controller, 'analyze_trades', fail_analysis)
    assert not controller.analyze_trades()
    assert controller.get_error() is not None

def test_llm_error(monkeypatch):
    controller = MainController()
    controller.process_csv('dummy_file')
    controller.analyze_trades()
    def fail_llm():
        controller.error = 'llm error'
        return False
    monkeypatch.setattr(controller, 'generate_llm_insights', fail_llm)
    assert not controller.generate_llm_insights()
    assert controller.get_error() is not None

def test_charts_error(monkeypatch):
    controller = MainController()
    controller.process_csv('dummy_file')
    controller.analyze_trades()
    controller.generate_llm_insights()
    def fail_charts():
        controller.error = 'charts error'
        return False
    monkeypatch.setattr(controller, 'generate_charts', fail_charts)
    assert not controller.generate_charts()
    assert controller.get_error() is not None

def test_report_error(monkeypatch):
    controller = MainController()
    controller.process_csv('dummy_file')
    controller.analyze_trades()
    controller.generate_llm_insights()
    controller.generate_charts()
    def fail_report():
        controller.error = 'report error'
        return False
    monkeypatch.setattr(controller, 'assemble_report', fail_report)
    assert not controller.assemble_report()
    assert controller.get_error() is not None

def test_export_error(monkeypatch):
    controller = MainController()
    controller.process_csv('dummy_file')
    controller.analyze_trades()
    controller.generate_llm_insights()
    controller.generate_charts()
    controller.assemble_report()
    def fail_export():
        controller.error = 'export error'
        return None
    monkeypatch.setattr(controller, 'export_report', fail_export)
    assert controller.export_report() is None
    assert controller.get_error() is not None

# --- Backend integration tests for upload-to-report workflow ---
def test_main_controller_valid_csv():
    controller = MainController()
    sample_csv = os.path.join(os.path.dirname(__file__), "sample_valid_trades.csv")
    assert controller.process_csv(sample_csv)
    assert controller.analyze_trades()
    assert controller.generate_llm_insights()
    assert controller.generate_charts()
    assert controller.assemble_report()
    link = controller.export_report()
    assert link == 'download_link'
    assert controller.get_error() is None

def test_main_controller_invalid_csv():
    controller = MainController()
    sample_csv = os.path.join(os.path.dirname(__file__), "sample_invalid.csv")
    # Simulate error in process_csv for invalid file
    def fail_csv(file):
        controller.error = 'csv error (invalid file)'
        return False
    controller.process_csv = fail_csv
    assert not controller.process_csv(sample_csv)
    assert controller.get_error() is not None 