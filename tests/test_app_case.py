# tests/test_app_case.py
#
# Simple, clear pytest examples.
# Show how to test file-writing functions without touching
# the real project folder, and how to avoid slow sleeps.
#
# Assumptions:
# - module is importable
# - pytest running from project root
#
# Run:
#   uv run python -m pytest


from pathlib import Path

from datafun_02_automation import app_case
import pytest


@pytest.fixture()
def temp_root_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Redirect app_case.ROOT_DIR to a temporary directory so tests
    do not write into the real working directory.
    """
    monkeypatch.setattr(app_case, "ROOT_DIR", tmp_path)
    return tmp_path


def test_write_text_file_creates_file(temp_root_dir: Path) -> None:
    path = temp_root_dir / "hello.txt"
    app_case.write_text_file(path, "Hi\n")

    assert path.exists()
    assert path.read_text(encoding="utf-8") == "Hi\n"


def test_create_files_for_range_writes_expected_files(temp_root_dir: Path) -> None:
    app_case.create_files_for_range(2020, 2022)

    for year in (2020, 2021, 2022):
        p = temp_root_dir / f"p02_year_{year}.txt"
        assert p.exists()
        assert (
            p.read_text(encoding="utf-8")
            == f"Project 02 generated file for year {year}\n"
        )


def test_create_files_from_list_writes_expected_files(temp_root_dir: Path) -> None:
    names = ["alpha", "beta"]
    app_case.create_files_from_list(names)

    for name in names:
        p = temp_root_dir / f"p02_list_{name}.txt"
        assert p.exists()
        assert (
            p.read_text(encoding="utf-8")
            == f"Project 02 generated file for item '{name}'\n"
        )


def test_create_prefixed_files_using_list_comprehension(temp_root_dir: Path) -> None:
    app_case.create_prefixed_files_using_list_comprehension(
        ["csv", "json"], prefix="out_"
    )

    for name in ("out_csv", "out_json"):
        p = temp_root_dir / f"p02_prefix_{name}.txt"
        assert p.exists()
        assert (
            p.read_text(encoding="utf-8")
            == f"Project 02 generated file for prefixed item '{name}'\n"
        )


def test_create_files_periodically_without_sleep(
    temp_root_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def _no_sleep(seconds: float) -> None:
        _ = seconds  # keep it obviously "used" for teaching
        return

    monkeypatch.setattr(app_case.time, "sleep", _no_sleep)

    app_case.create_files_periodically(wait_seconds=99, count=3)

    for i in (1, 2, 3):
        p = temp_root_dir / f"p02_periodic_{i:02d}.txt"
        assert p.exists()
        assert p.read_text(encoding="utf-8") == f"Project 02 periodic file number {i}\n"


def test_create_standardized_files_lowercase_and_remove_spaces(
    temp_root_dir: Path,
) -> None:
    names = ["North America", "Middle East"]
    app_case.create_standardized_files(names, to_lowercase=True, remove_spaces=True)

    expected = {
        "North America": "northamerica",
        "Middle East": "middleeast",
    }

    for original, standardized in expected.items():
        p = temp_root_dir / f"p02_region_{standardized}.txt"
        assert p.exists()
        assert p.read_text(encoding="utf-8") == (
            f"Project 02 standardized file for '{original}' -> '{standardized}'\n"
        )
