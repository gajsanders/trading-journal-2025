from typing import Dict, List
from src.reports.markdown_generator import MarkdownGenerator

class ReportAssembler:
    """
    Assembles complete monthly reports from all components.
    """
    @staticmethod
    def assemble_report(metrics: Dict, charts_md: str, insights: str, questions: List[str], action_items: List[str]) -> str:
        return MarkdownGenerator.generate_report(metrics, charts_md, insights, questions, action_items) 