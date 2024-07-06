from os import environ
from pathlib import Path

HOME_DIR = Path(environ["HOME"])
CONFIG_DIR = HOME_DIR / ".alfred_snippet_manager"

if not CONFIG_DIR.exists():
    CONFIG_DIR.mkdir()

REPO_DIR = CONFIG_DIR / "repository"
if not REPO_DIR.exists():
    REPO_DIR.mkdir()

SETTING_PATH = CONFIG_DIR / "setting.json"
