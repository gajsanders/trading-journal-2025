import os
from typing import Optional

class ExportHandler:
    """
    Handles saving and exporting markdown reports.
    """
    @staticmethod
    def save_report(markdown: str, path: str) -> str:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        return path

    @staticmethod
    def get_download_link(path: str) -> Optional[str]:
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        import base64
        b64 = base64.b64encode(content.encode()).decode()
        return f'<a href="data:text/markdown;base64,{b64}" download="report.md">Download Report</a>' 