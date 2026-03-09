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
    has_oss_stack = all(
        f in fonts_output for f in ["CourierPrime", "NotoSerifCJKsc", "LXGWWenKaiGB"]
    ) and any(f in fonts_output for f in ["NotoSansCJKsc", "FandolHei"])

    has_latin_standard = any(
        m in fonts_output for m in ["TimesNewRoman", "Times-Roman", "Tinos", "texgyretermes"]
    ) and any(
        m in fonts_output for m in ["CourierNew", "CourierPrime", "lmmono", "LMMono"]
    )

    has_song = any(m in fonts_output for m in [
        "SimSun", "STSong", "FZShuSong", "FZSSK", "HYShuSongErKW", "NotoSerifCJKsc", "FandolSong",
    ])
    has_kai = any(m in fonts_output for m in [
        "KaiTi_GB2312", "KaiTi", "STKaiti", "HYKaiTi", "HYc1gj", "LXGWWenKaiGB", "FandolKai",
    ])
    has_hei = any(m in fonts_output for m in [
        "SimHei", "STHeiti", "HYZhongJianHei", "HYZhongHeiKW", "HYQiHei", "NotoSansCJKsc", "FandolHei",
    ])
    has_standard_cjk = has_song and has_kai and has_hei

    assert has_oss_stack or (has_latin_standard and has_standard_cjk), \
        "main.pdf 未嵌入可接受的标准学术字体栈（正文/楷体/黑体/西文字体）。"
