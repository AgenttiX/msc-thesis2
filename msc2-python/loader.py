"""Add PTtools to PATH

This can be done directly in PyCharm by going to Settings -> Project -> Project Structure
"""

import os.path
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PTTOOLS_DIR = os.path.join(os.path.dirname(REPO_DIR), "pttools")
if not os.path.isdir(PTTOOLS_DIR):
    raise NotADirectoryError(f"PTtools directory not found: {PTTOOLS_DIR}")


def load():
    sys.path.insert(1, PTTOOLS_DIR)
