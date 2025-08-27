from typing import Dict, List
from src.reports import report_templates as templates

class MarkdownGenerator:
    """
    Generates markdown reports for monthly trading summaries.
    """
    @staticmethod
    def generate_report(metrics: Dict, charts_md: str, insights: str, questions: List[str], action_items: List[str]) -> str:
        md = []
        md.append(templates.METRICS_TEMPLATE.render(**metrics))
        md.append(templates.CHARTS_TEMPLATE.render(charts_md=charts_md))
        md.append(templates.INSIGHTS_TEMPLATE.render(insights=insights))
        md.append(templates.REFLECTION_TEMPLATE.render(questions=questions))
        md.append(templates.ACTIONS_TEMPLATE.render(action_items=action_items))
        return '\n\n'.join(md) 