from src.reports.markdown_generator import MarkdownGenerator

def test_generate_report():
    metrics = {
        'win_rate': 0.7,
        'total_pnl': 1500,
        'time_weighted_return': 0.18,
        'risk_adjusted_return': 2.1
    }
    charts_md = '![chart](data:image/png;base64,abc123)'
    insights = "Performance was strong this month."
    questions = ["What worked well?", "What will you change?"]
    action_items = ["Reduce position size", "Review losing trades"]
    md = MarkdownGenerator.generate_report(metrics, charts_md, insights, questions, action_items)
    assert "Key Metrics Overview" in md
    assert "- **Win Rate:** 0.7" in md
    assert "Visual Section" in md
    assert charts_md in md
    assert "Detailed Analysis Section" in md
    assert insights in md
    assert "Monthly Reflection Questions" in md
    assert questions[0] in md
    assert "Action Items and Improvement Areas" in md
    assert action_items[0] in md

def test_generate_report_empty():
    md = MarkdownGenerator.generate_report({}, '', '', [], [])
    assert "Key Metrics Overview" in md
    assert "Visual Section" in md
    assert "Detailed Analysis Section" in md
    assert "Monthly Reflection Questions" in md
    assert "Action Items and Improvement Areas" in md 