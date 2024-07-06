import json
from pathlib import Path

from alfred_snippet_manager.models.snippet import Snippet


def test_load(snippet_path: Path):
    snippet = Snippet.load(snippet_path)
    assert snippet


def test_eq(snippet_path: Path):
    snippet1 = Snippet.load(snippet_path)
    snippet2 = Snippet.load(snippet_path)
    assert snippet1 == snippet2


def test_is_same_item(snippet_path: Path):
    snippet1 = Snippet.load(snippet_path)
    snippet2 = Snippet.load(snippet_path)
    snippet2.snippet = ""
    assert snippet1 != snippet2
    assert snippet1.is_same_item(snippet2)


def test_to_json_str(snippet_path: Path):
    snippet = Snippet.load(snippet_path)
    json_str = snippet.to_json_str()
    json_obj = json.loads(json_str)
    assert snippet.keyword == json_obj["alfredsnippet"]["keyword"]


def test_generate_from_file(snippet_path: Path, snippet_file_path:Path):
    snippet1 = Snippet.load(snippet_path)
    snippet2 = Snippet.generate_from_file(snippet_file_path)
    assert snippet1 == snippet2
