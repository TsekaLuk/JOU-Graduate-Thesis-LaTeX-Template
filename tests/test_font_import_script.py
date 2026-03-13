#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import import_fonts


def test_default_search_dirs_include_desktop_font_folder_when_present():
    dirs = import_fonts.default_search_dirs()
    expected = Path.home() / "Desktop" / "毕业论文字体"
    if expected.exists():
        assert expected in dirs


def test_parse_args_supports_undergrad_parity_flags():
    args = import_fonts.parse_args(
        ["--search-dir", "/tmp/fonts", "--force", "--dry-run", "--skip-optional"]
    )
    assert args.search_dir == ["/tmp/fonts"]
    assert args.force is True
    assert args.dry_run is True
    assert args.skip_optional is True


def test_import_fonts_normalizes_common_font_names(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "黑体.ttf").write_bytes(b"simhei")
    (source / "华文行楷.ttf").write_bytes(b"xingkai")
    (source / "华文隶书.ttf").write_bytes(b"lishu")

    target = tmp_path / "target"
    result = import_fonts.import_fonts([source], target)

    assert (target / "SimHei.ttf").exists()
    assert (target / "STXingkai.ttf").exists()
    assert (target / "STLiti.ttf").exists()
    assert any("黑体" in item for item in result["copied"])


def test_import_fonts_can_skip_optional_fonts(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "华文隶书.ttf").write_bytes(b"lishu")

    target = tmp_path / "target"
    result = import_fonts.import_fonts([source], target, include_optional=False)

    assert not (target / "STLiti.ttf").exists()
    for bucket in result.values():
        assert all("华文隶书" not in item for item in bucket)


def test_import_fonts_dry_run_does_not_copy_files(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "Times New Roman.ttf").write_bytes(b"times")

    target = tmp_path / "target"
    result = import_fonts.import_fonts([source], target, dry_run=True)

    assert not (target / "TimesNewRoman-Regular.ttf").exists()
    assert any("Times New Roman Regular" in item for item in result["planned"])
