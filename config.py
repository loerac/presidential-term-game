from pathlib import Path, PosixPath

CURRENT_DIR = Path.cwd()
CSS_DIR = Path.joinpath(CURRENT_DIR, "css")


def get_css_path(file_name: str) -> PosixPath:
    """Get the file path to the CSS"""
    return Path.joinpath(CSS_DIR, file_name)
