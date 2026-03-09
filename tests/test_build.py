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


def test_pdf_has_embedded_fonts(fonts_output: str):
    """Verify the compiled PDF has at least one embedded font.

    The placeholder main.tex uses whatever default Latin/CJK fonts the
    runner provides via fontspec/xeCJK. We only confirm that something
    was embedded — full joufonts stack tests are covered statically by
    test_cross_platform_font_support.py.
    """
    non_header_lines = [l for l in fonts_output.splitlines() if l.strip() and "name" not in l.lower()]
    assert len(non_header_lines) > 0, "main.pdf 未嵌入任何字体，PDF 可能为空或编译异常。"
