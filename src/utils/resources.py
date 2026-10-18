from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def resource_path(relative_path):
    """Absolute path of a project file, independent of the current working directory."""
    return str(PROJECT_ROOT / relative_path)
