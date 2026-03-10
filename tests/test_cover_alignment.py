#!/usr/bin/env python3
"""Focused cover-page alignment checks against the reference PDF."""

from __future__ import annotations

from conftest import REFERENCE_PDF, MAIN_PDF, find_line_containing, line_center


def _assert_line_close(template_pdf, template_page, reference_pdf, reference_page, phrase, *, x_tol, y_tol):
    template_line = find_line_containing(template_pdf, template_page, phrase)
    reference_line = find_line_containing(reference_pdf, reference_page, phrase)
    assert template_line is not None, f"模板页面未找到短语: {phrase}"
    assert reference_line is not None, f"参考页面未找到短语: {phrase}"

    template_center = line_center(template_line)
    reference_center = line_center(reference_line)

    assert abs(template_center[0] - reference_center[0]) <= x_tol, (
        f"短语 {phrase} 的水平位置偏差过大: 模板={template_center[0]:.1f}, 参考={reference_center[0]:.1f}"
    )
    assert abs(template_center[1] - reference_center[1]) <= y_tol, (
        f"短语 {phrase} 的垂直位置偏差过大: 模板={template_center[1]:.1f}, 参考={reference_center[1]:.1f}"
    )


def test_cover_title_alignment():
    _assert_line_close(MAIN_PDF, 1, REFERENCE_PDF, 1, "硕士学位论文", x_tol=15, y_tol=60)
    _assert_line_close(MAIN_PDF, 1, REFERENCE_PDF, 1, "浮选旋流分选机理研究", x_tol=20, y_tol=30)
    _assert_line_close(MAIN_PDF, 1, REFERENCE_PDF, 1, "江苏海洋大学", x_tol=20, y_tol=120)


def test_inner_cover_alignment():
    _assert_line_close(MAIN_PDF, 3, REFERENCE_PDF, 3, "江苏海洋大学", x_tol=20, y_tol=35)
    _assert_line_close(MAIN_PDF, 3, REFERENCE_PDF, 3, "硕士学位论文", x_tol=25, y_tol=40)
    _assert_line_close(MAIN_PDF, 3, REFERENCE_PDF, 3, "浮选旋流分选机理研究", x_tol=25, y_tol=45)
