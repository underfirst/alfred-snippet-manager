from pathlib import Path
from shutil import rmtree
from subprocess import run

from loguru import logger

from alfred_snippet_manager.configs.datapath import REPO_DIR, SETTING_PATH
from alfred_snippet_manager.models.setting import Setting
from alfred_snippet_manager.models.snippet import Snippet


class AlfredSnippetManager:
    def __init__(self,
                 setting_path: Path = SETTING_PATH,
                 repo_dir:Path = REPO_DIR):
        self.setting_path = setting_path
        self.repo_dir = repo_dir
    def _load_setting(self) -> Setting:
        return Setting.load(self.setting_path)

    def _dump_setting(self, setting: Setting) -> None:
        setting.dump(self.setting_path)

    def get_preference_path(self) -> Path:
        setting = self._load_setting()
        return setting.get_preference_path(self.setting_path)

    def load_gitignore(self, directory: Path) -> list[str]:
        ignore_path = directory / ".gitignore"
        ret = []
        if ignore_path.exists():
            for line in ignore_path.read_text().split("\n"):
                line = line.strip()
                if line.startswith("#") or len(line) == 0:
                    continue
                ret.append(line)
        return ret

    def load_snippets_from_preference(self) -> list[Snippet]:
        preference_path = self.get_preference_path()
        snippet_path = preference_path / "snippets"
        if not snippet_path.is_dir():
            msg = "The alfred snippets directory is invalid."
            raise ValueError(msg)
        ret = []
        for file in snippet_path.glob("**/*.json"):
            data = Snippet.load(file)
            if data is not None:
                ret.append(data)
        return ret

    def generate_snippets_from_repos(self) -> list[Snippet]:
        directories = self.get_snippet_directories()
        ret = []

        for directory in directories:
            for path in directory.glob("snippet_resources/**/*"):
                if path.is_file():
                    # TODO: filter matched ignore pattern
                    snippet = Snippet.generate_from_file(path)
                    if isinstance(snippet, Snippet):
                        ret.append(snippet)
        return ret

    def get_diff(self) -> tuple[list[Snippet], list[Snippet]]:
        current_snippets = set(self.load_snippets_from_preference())
        repo_snippets = self.generate_snippets_from_repos()
        updated_snippets = []
        new_snippets = []
        for repo_snippet in repo_snippets:
            if repo_snippet in current_snippets:
                continue
            is_updated = False
            for current_snippet in current_snippets:
                if repo_snippet.is_same_item(current_snippet):
                    repo_snippet.name = current_snippet.name
                    repo_snippet.path_name = current_snippet.path_name
                    repo_snippet.uid = current_snippet.uid
                    repo_snippet.collections = current_snippet.collections
                    updated_snippets.append(repo_snippet)
                    is_updated = True
                    break
            if not is_updated:
                new_snippets.append(repo_snippet)
        return new_snippets, updated_snippets



    def get_snippet_directories(self) -> list[Path]:
        setting = self._load_setting()
        ret = []
        for repo in setting.repo:
            repo_dir = setting.convert_repo_path(repo, self.repo_dir)
            if repo_dir.exists() and repo_dir.is_dir():
                ret.append(repo_dir)
            else:
                logger.warning(f"Repo directory {repo_dir} is not exists. Might need sync-repos.")
        for directory in setting.directories:
            if directory.exists() and directory.is_dir():
                ret.append(directory)
        if len(ret) == 0:
            msg = "There is no snippet directories. Add repo/directories to setting."
            raise ValueError(msg)
        return ret

    def add_repo(self, repo: str) -> None:
        setting = self._load_setting()
        if repo not in setting.repo:
            logger.info(f"Add repo: {repo}")
            setting.repo.append(repo)
        else:
            logger.info("Repo is already in setting.")
            pass
        self._dump_setting(setting)

    def add_local(self, local_directory: Path) -> None:
        setting = self._load_setting()
        if local_directory not in setting.directories:
            logger.info(f"Add directory: {local_directory.absolute()}")
            setting.directories.append(local_directory)
        else:
            logger.info("Directory is already in setting.")
            pass
        self._dump_setting(setting)

    def sync_repos(self) -> None:
        setting = self._load_setting()
        rmtree(self.repo_dir, ignore_errors=True)
        self.repo_dir.mkdir(parents=True, exist_ok=True)
        for repo in setting.repo:
            run(
                f"""cd {self.repo_dir!s};
                        git clone {repo}""",
                shell=True,
                capture_output=True,
                text=True, check=False,
            )

    def update(self) -> None:
        new_snippets, updated_snippets = self.get_diff()
        preference_path = self.get_preference_path()
        snippet_dir = preference_path / "snippets"
        for snippet in new_snippets:
            collection_path = snippet_dir / snippet.collections
            if not collection_path.exists():
                collection_path.mkdir()
            with open(collection_path / snippet.path_name, "w") as f:
                f.write(snippet.to_json_str())
        for snippet in updated_snippets:
            snippet_path = snippet_dir / snippet.collections / snippet.path_name
            with open(snippet_path, "w") as f:
                f.write(snippet.to_json_str())
