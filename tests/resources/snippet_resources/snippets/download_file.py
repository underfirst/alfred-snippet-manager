from pathlib import Path

import requests


def download_file(url: str, filepath: str | Path):
    ret = requests.get(url, timeout=3600)
    if ret.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(ret.content)
