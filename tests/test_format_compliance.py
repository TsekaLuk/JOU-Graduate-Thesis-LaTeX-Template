#!/usr/bin/env python3
"""Static format and repository-contract checks for the graduate template."""

from __future__ import annotations

from conftest import CLASS_FILE, HEADINGS_FILE, MAIN_FILE


def test_main_uses_graduate_class():
    assert "\\documentclass{styles/jougraduate}" in MAIN_FILE.read_text(encoding="utf-8")


def test_class_declares_expected_geometry():
    content = CLASS_FILE.read_text(encoding="utf-8")
    for marker in [
        "top=2.54cm",
        "bottom=2.54cm",
        "left=3.18cm",
        "right=3.18cm",
        "ctexbook",
        "JOUApplySharedMetadata",
    ]:
        assert marker in content, f"jougraduate.cls 缺少关键格式标记: {marker}"


def test_headings_fix_toc_depth_and_header_text():
    content = HEADINGS_FILE.read_text(encoding="utf-8")
    assert "setcounter{tocdepth}{1}" in content, "目录深度应固定到二级标题"
    assert "江苏海洋大学硕士学位论文" in content, "页眉文本未切换到研究生模板"


def test_dataset_page_contains_required_fields(thesis_pages: dict[int, str]):
    dataset = thesis_pages[19]
    for marker in [
        "学位论文数据集",
        "学位授予单位名称",
        "学位授予单位代码",
        "论文题名",
        "作者姓名",
        "导师姓名",
    ]:
        assert marker in dataset, f"数据集页面缺少字段: {marker}"
