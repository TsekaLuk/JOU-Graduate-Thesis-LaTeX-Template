#!/usr/bin/env python3
"""Basic build regression checks for the graduate thesis template."""

from __future__ import annotations

import subprocess

import pytest

from conftest import MAIN_PDF, pdf_page_count, pdffonts


# ── Build output ────────────────────────────────────────────────────────────

def test_main_pdf_exists():
    assert MAIN_PDF.exists(), "缺少 main.pdf，论文未成功编译"


def test_main_pdf_is_nonempty():
    assert MAIN_PDF.stat().st_size > 1024, "main.pdf 体积异常（< 1 KB），疑似空文件"


def test_main_pdf_page_count():
    assert pdf_page_count(MAIN_PDF) == 19, "当前主模板页数与研究生论文合同不一致"


# ── Font stack ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def fonts_output() -> str:
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    return pdffonts(MAIN_PDF)


def test_pdf_has_embedded_fonts(fonts_output: str):
    non_header_lines = [l for l in fonts_output.splitlines() if l.strip() and "name" not in l.lower()]
    assert len(non_header_lines) > 0, "main.pdf 未嵌入任何字体，PDF 可能为空或编译异常。"
