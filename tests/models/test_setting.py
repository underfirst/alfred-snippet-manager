import tempfile
from pathlib import Path

from alfred_snippet_manager.models.setting import Setting


def test_load(resource_path: Path):
    setting = Setting.load(resource_path / "test_setting.json")
    assert setting.preference_path.exists()


def test_dump(resource_path: Path):
    setting = Setting.load(resource_path / "test_setting.json")
    with tempfile.TemporaryDirectory() as dir_name:
        test_path = Path(dir_name) / "dumped_setting.json"
        setting.dump(test_path)
        loaded = Setting.load(test_path)
        assert loaded.preference_path == setting.preference_path


def test_convert_repo_path(resource_path: Path):
    setting = Setting.load(resource_path / "test_setting.json")
    setting.convert_repo_path(setting.repo[0])
    assert isinstance(setting.convert_repo_path(setting.repo[0]), Path)
    assert setting.convert_repo_path(setting.repo[0]).name == "alfred-snippet-manager"
