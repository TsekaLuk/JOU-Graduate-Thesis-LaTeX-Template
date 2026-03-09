#!/usr/bin/env python3
"""
Basic build regression checks for the JOU graduate thesis template.

Verifies that:
- main.pdf was successfully produced by the build step
- The embedded font stack meets the minimum academic requirements
"""

from __future__ import annotations

import subprocess

import pytest

from conftest import MAIN_PDF, pdffonts


# ── Build output ────────────────────────────────────────────────────────────

def test_main_pdf_exists():
    assert MAIN_PDF.exists(), "缺少 main.pdf，论文未成功编译"


def test_main_pdf_is_nonempty():
    assert MAIN_PDF.stat().st_size > 1024, "main.pdf 体积异常（< 1 KB），疑似空文件"


# ── Font stack ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def fonts_output() -> str:
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    return pdffonts(MAIN_PDF)


def test_pdf_has_acceptable_font_stack(fonts_output: str):
    """Verify at least one Latin and one CJK font are embedded.

    A minimal placeholder document may not exercise the full font stack
    (e.g. monospace/heading fonts only appear when actually used). We
    therefore check only that the main body Latin and CJK fonts are present.
    """
    has_latin = any(m in fonts_output for m in [
        "TimesNewRoman", "Times-Roman", "Tinos", "texgyretermes",
        "STSong", "SimSun",
    ])
    has_cjk = any(m in fonts_output for m in [
        "NotoSerifCJKsc", "FandolSong", "SimSun", "STSong",
        "FZShuSong", "FZSSK", "HYShuSongErKW",
        "NotoSansCJKsc", "FandolHei", "SimHei", "STHeiti",
        "LXGWWenKaiGB", "FandolKai", "KaiTi", "STKaiti",
    ])

    assert has_latin, "main.pdf 未嵌入任何可接受的西文正文字体（Tinos/Times 等）。"
    assert has_cjk, "main.pdf 未嵌入任何可接受的 CJK 字体（NotoSerifCJKsc/FandolSong 等）。"
