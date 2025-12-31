import os
import shutil

def ensure_dir(path: str):
    """
    Ensure that a directory exists. If not, create it.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def file_exists(path: str) -> bool:
    """
    Check if a file exists.
    """
    return os.path.isfile(path)
