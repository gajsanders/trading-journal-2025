import os
import tempfile
from src.reports.export_handler import ExportHandler

def test_save_report_and_read():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'report.md')
        content = "# Report\nSome content."
        saved_path = ExportHandler.save_report(content, path)
        assert os.path.exists(saved_path)
        with open(saved_path, 'r', encoding='utf-8') as f:
            assert f.read() == content

def test_get_download_link():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'report.md')
        content = "# Report\nSome content."
        ExportHandler.save_report(content, path)
        link = ExportHandler.get_download_link(path)
        assert link.startswith('<a href="data:text/markdown;base64,')
        assert 'download="report.md"' in link

def test_get_download_link_missing():
    link = ExportHandler.get_download_link('/tmp/nonexistent_file.md')
    assert link is None 