import sys
import importlib

def test_python_version():
    # M1 Mac recommended: Python 3.9+
    major, minor = sys.version_info[:2]
    assert major == 3 and minor >= 9

def test_dependencies_importable():
    # Try to import all key dependencies
    for pkg in [
        "pandas", "streamlit", "matplotlib", "seaborn", "openai", "jinja2", "pytest", "dotenv"
    ]:
        importlib.import_module(pkg) 