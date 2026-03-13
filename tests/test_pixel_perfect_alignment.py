#!/usr/bin/env python3
"""Cross-page position checks for stable layout anchors."""

from __future__ import annotations

import pytest

from conftest import MAIN_PDF, REFERENCE_PDF, find_line_containing, line_center


ALIGNMENT_CASES = [
    {"id": "program-appendix-title", "template_page": 22, "reference_page": 19, "phrase": "附录1", "x_tol": 20, "y_tol": 25},
    {"id": "author-resume-first-section", "template_page": 23, "reference_page": 20, "phrase": "一、基本情况", "x_tol": 25, "y_tol": 30},
    {"id": "originality-signature", "template_page": 24, "reference_page": 21, "phrase": "学位论文作者签字：", "x_tol": 24, "y_tol": 18},
    {"id": "dataset-first-field", "template_page": 25, "reference_page": 22, "phrase": "关键词*", "x_tol": 40, "y_tol": 35},
    {"id": "dataset-org-field", "template_page": 25, "reference_page": 22, "phrase": "学位授予单位名称", "x_tol": 45, "y_tol": 60}
]


@pytest.mark.parametrize("case", ALIGNMENT_CASES, ids=lambda case: case["id"])
def test_reference_anchor_positions(case: dict):
    template_line = find_line_containing(MAIN_PDF, case["template_page"], case["phrase"])
    reference_line = find_line_containing(REFERENCE_PDF, case["reference_page"], case["phrase"])
    assert template_line is not None, f"[{case['id']}] 模板中缺少短语 {case['phrase']}"
    assert reference_line is not None, f"[{case['id']}] 参考中缺少短语 {case['phrase']}"

    template_center = line_center(template_line)
    reference_center = line_center(reference_line)
    assert abs(template_center[0] - reference_center[0]) <= case["x_tol"], (
        f"[{case['id']}] 水平偏差过大: 模板={template_center[0]:.1f}, 参考={reference_center[0]:.1f}"
    )
    assert abs(template_center[1] - reference_center[1]) <= case["y_tol"], (
        f"[{case['id']}] 垂直偏差过大: 模板={template_center[1]:.1f}, 参考={reference_center[1]:.1f}"
    )
