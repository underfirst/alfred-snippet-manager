from pathlib import Path

import pytest


@pytest.fixture()
def resource_path() -> Path:
    path = Path(__file__).parent / "resources"
    if path.exists():
        return path
    msg = "path is not invalid."
    raise ValueError(msg)


@pytest.fixture()
def snippet_path() -> Path:
    return Path(__file__).parent / "resources/snippets/test.json"


@pytest.fixture()
def snippet_resource_path() -> Path:
    return Path(__file__).parent / "resources/snippet_resources/"


@pytest.fixture()
def snippet_file_path() -> Path:
    return Path(__file__).parent / "resources/snippet_resources/snippets/download_file.py"
