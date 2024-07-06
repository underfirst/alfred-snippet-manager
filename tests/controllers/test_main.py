from pathlib import Path

from alfred_snippet_manager.controllers.main import AlfredSnippetManager
from alfred_snippet_manager.models.setting import Setting
from alfred_snippet_manager.models.snippet import Snippet


def omit_setting():
    resource_path = Path(__file__).parent.parent / "resources"
    setting_dir = resource_path / "test_setting"
    Setting.clear_setting(setting_path=setting_dir / "test_setting.json")
    setting = Setting.load(setting_dir / "test_setting.json")
    setting.preference_path = resource_path / "Alfred.alfredpreferences"
    setting.dump(setting_dir / "test_setting.json")
    return setting

def omit_asm():
    resource_path = Path(__file__).parent.parent / "resources"
    setting_dir = resource_path / "test_setting"
    repo_dir = setting_dir / "repo"
    repo_dir.mkdir(parents=True, exist_ok=True)
    asm = AlfredSnippetManager(setting_path=setting_dir / "test_setting.json",
                               repo_dir=repo_dir)
    omit_setting()
    return asm


def test_load_snippets_from_preferences():
    mgr = omit_asm()
    snippets = mgr.load_snippets_from_preference()
    assert len(snippets) > 0


def test_add_local_and_get_snippet_directories(
        snippet_resource_path: Path):
    mgr = omit_asm()
    mgr.load_snippets_from_preference()
    mgr.add_local(snippet_resource_path.parent)
    ret = mgr.get_snippet_directories()
    assert len(ret) == 1


def test_generate_snippets_from_repos(snippet_resource_path: Path):
    mgr = omit_asm()
    mgr.load_snippets_from_preference()
    mgr.add_local(snippet_resource_path.parent)
    ret = mgr.generate_snippets_from_repos()
    assert len(ret) == 3


def test_add_repo_and_sync_repo():
    mgr = omit_asm()
    mgr.add_repo("https://github.com/underfirst/example_snippets.git")  # TODO: create
    mgr.sync_repos()
    directories = mgr.get_snippet_directories()
    directory_names = [d.name for d in directories]
    assert "example_snippets" in directory_names


def test_get_diff(snippet_resource_path:Path):
    mgr = omit_asm()
    mgr.add_local(snippet_resource_path.parent)
    ret = mgr.get_diff()
    assert isinstance(ret, tuple)
    assert len(ret[0]) == 1 and len(ret[1]) == 1

def test_update():
    # TODO
    pass
