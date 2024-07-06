import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from shutil import rmtree

from loguru import logger

from alfred_snippet_manager.configs.datapath import HOME_DIR, REPO_DIR, SETTING_PATH


@dataclass
class Setting:
    preference_path: Path | None = None
    repo: list[str] = field(default_factory=list)
    directories: list[Path] = field(default_factory=list)

    @classmethod
    def load(cls, setting_path: Path = SETTING_PATH):
        if not setting_path.exists():
            logger.warning("Initialize .alfred_snippet_manager to $HOME directory.")
            Setting().dump(setting_path)
        try:
            setting_dict = json.loads(setting_path.read_text())
        except json.JSONDecodeError:
            msg = "Setting file is invalid json."
            raise ValueError(msg)
        setting_dict["directories"] = [Path(d) for d in setting_dict["directories"]]
        if setting_dict.get("preference_path", None) is not None:
            setting_dict["preference_path"] = Path(setting_dict["preference_path"])
        return Setting(**setting_dict)

    @classmethod
    def clear_setting(cls, setting_path: Path=SETTING_PATH):
        rmtree(setting_path.parent)

    def dump(self, setting_path: Path = SETTING_PATH):

        setting_dict = asdict(self)
        setting_dict["directories"] = [str(d) for d in setting_dict["directories"]]
        if setting_dict.get("preference_path", None) is None:
            setting_dict["preference_path"] = None
        else:
            setting_dict["preference_path"] = str(setting_dict["preference_path"])
        if not setting_path.parent.exists():
            setting_path.parent.mkdir()
        with open(setting_path, "w") as f:
            json.dump(setting_dict, f)

    def get_preference_path(self, setting_path:Path=SETTING_PATH) -> Path:
        if self.preference_path is not None and self.preference_path.is_dir():
            return self.preference_path

        default_path = HOME_DIR / "Library/Application Support/Alfred/Alfred.alfredpreferences"
        if not default_path.exists():
            self.preference_path = default_path
            self.dump(setting_path)
            return default_path
        for path in HOME_DIR.glob("**/Alfred.alfredpreferences"):
            if path.is_dir() and path.name == "Alfred.alfredpreferences":
                self.preference_path = path
                self.dump(setting_path)
                return path
        msg = "Alfred.alfredpreferences path is not in HOME directory. Add the path to the config."
        raise ValueError(msg)


    def convert_repo_path(self, repo: str, repo_dir:Path=REPO_DIR) -> Path:
        return repo_dir / repo.split("/")[-1].replace(".git", "")
