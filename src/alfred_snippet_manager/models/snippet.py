import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4


@dataclass()
class Snippet:
    uid: str
    name: str
    snippet: str
    keyword: str
    path_name: str
    collections: str = "default"

    def __eq__(self, other) -> bool:
        return (
            self.name == other.name
            and self.snippet == other.snippet
            and self.keyword == other.keyword
            and self.collections == other.collections
        )

    def __hash__(self):
        return hash((self.name, self.keyword, self.collections, self.snippet))

    def is_same_item(self, other) -> bool:
        return self.keyword == other.keyword and self.collections == other.collections

    def to_json_str(self):
        return json.dumps(
            {
                "alfredsnippet": {
                    "uid": str(uuid4()).upper(),
                    "name": self.name,
                    "snippet": self.snippet,
                    "keyword": self.keyword,
                }
            },
            ensure_ascii=False,
            indent=2,
        )

    @classmethod
    def generate_from_file(cls, path: Path):
        if path.exists():
            snippet = path.read_text()
            name = path.name
            if name.startswith("!"):
                name = name[1:]
            else:
                name = ".".join(name.split(".")[:-1])
            keyword = name
            uid = str(uuid4()).upper()
            return Snippet(
                uid=uid,
                name=name,
                keyword=keyword,
                snippet=snippet,
                collections=path.parent.name,
                path_name=uid + ".json",
            )

        return None

    @classmethod
    def load(cls, path: Path):
        if path.exists():
            try:
                text = path.read_text()
                data = json.loads(text)
                if data.get("alfredsnippet", None) is None:
                    return None
                data = data["alfredsnippet"]
                return Snippet(
                    uid=data.get("uid", str(uuid4()).upper()),
                    name=data.get("name", ""),
                    snippet=data.get("snippet", ""),
                    keyword=data.get("keyword", ""),
                    collections=path.parent.name,
                    path_name=path.name,
                )
            except json.JSONDecodeError:
                return None
        return None
