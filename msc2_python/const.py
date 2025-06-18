import os


REPO_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR: str = os.path.join(REPO_DIR, "fig")
LOG_DIR: str = os.path.join(REPO_DIR, "logs")

if not os.path.exists(FIG_DIR):
    os.mkdir(FIG_DIR)

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
