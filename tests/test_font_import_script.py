#!/usr/bin/env python3

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import import_fonts


def test_build_search_dirs_includes_desktop_font_folder():
    dirs = import_fonts.build_search_dirs()
    expected = Path.home() / "Desktop" / "毕业论文字体"
    if expected.exists():
        assert expected in dirs


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
    assert any(item.startswith("SimHei.ttf <- ") for item in result["copied"])
