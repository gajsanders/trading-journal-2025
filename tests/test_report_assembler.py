import pytest
from src.reports import report_assembler
from src.reports.report_assembler import ReportAssembler

def test_assemble_report(monkeypatch):
    class DummyMarkdownGenerator:
        @staticmethod
        def generate_report(metrics, charts_md, insights, questions, action_items):
            return f"## Key Metrics Overview\n{metrics}\n{charts_md}\n{insights}\n{questions}\n{action_items}"
    monkeypatch.setattr(report_assembler, 'MarkdownGenerator', DummyMarkdownGenerator)
    metrics = {'pnl': 100, 'win_rate': 0.7}
    charts_md = "![chart](url)"
    insights = "Great month!"
    questions = ["What worked?", "What to improve?"]
    actions = ["Review losers", "Size up winners"]
    result = ReportAssembler.assemble_report(metrics, charts_md, insights, questions, actions)
    assert "## Key Metrics Overview" in result
    assert str(metrics) in result
    assert charts_md in result
    assert insights in result
    assert str(questions) in result
    assert str(actions) in result

def test_assemble_report_empty(monkeypatch):
    class DummyMarkdownGenerator:
        @staticmethod
        def generate_report(metrics, charts_md, insights, questions, action_items):
            return f"## Key Metrics Overview\n{metrics}\n{charts_md}\n{insights}\n{questions}\n{action_items}"
    monkeypatch.setattr(report_assembler, 'MarkdownGenerator', DummyMarkdownGenerator)
    result = ReportAssembler.assemble_report({}, "", "", [], [])
    assert "## Key Metrics Overview" in result
    assert '{}' in result

def test_assemble_report_error(monkeypatch):
    class FailingMarkdownGenerator:
        @staticmethod
        def generate_report(*a, **kw):
            raise Exception("fail")
    monkeypatch.setattr(report_assembler, 'MarkdownGenerator', FailingMarkdownGenerator)
    with pytest.raises(Exception):
        ReportAssembler.assemble_report({}, "", "", [], []) 