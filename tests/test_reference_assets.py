#!/usr/bin/env python3
"""Reference asset contract for the graduate thesis alignment baseline."""

from __future__ import annotations

from conftest import (
    REFERENCE_DOC,
    REFERENCE_DOCX,
    REFERENCE_PDF,
    REFERENCE_XML,
    get_pdfinfo,
    pdf_page_count,
)


def test_reference_source_files_exist():
    assert REFERENCE_DOC.exists(), "缺少原始参考 .doc 文件"
    assert REFERENCE_DOCX.exists(), "缺少转换后的参考 .docx 文件"
    assert REFERENCE_PDF.exists(), "缺少 WPS 导出的参考 PDF"
    assert REFERENCE_XML.exists(), "缺少解包后的 word/document.xml"


def test_reference_pdf_contract(reference_spec: dict):
    assert pdf_page_count(REFERENCE_PDF) == reference_spec["reference"]["expected_pages"], "参考 PDF 页数异常"
    info = get_pdfinfo(REFERENCE_PDF)
    assert "A4" in info["Page size"], "参考 PDF 不是 A4"
    assert "WPS Writer" in info["Creator"], "参考 PDF 不是 WPS 导出基线"


def test_reference_xml_has_expected_markers():
    content = REFERENCE_XML.read_text(encoding="utf-8")
    for marker in [
        "硕士学位论文",
        "学位论文使用授权声明",
        "论文审阅认定书",
        "致谢",
        "Abstract",
        "Extended Abstract",
        "参考文献",
        "作者简历",
        "学位论文数据集",
    ]:
        assert marker in content, f"word/document.xml 缺少关键标记: {marker}"
