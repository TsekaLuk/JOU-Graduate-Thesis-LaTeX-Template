#!/usr/bin/env python3
"""Cross-page position checks for stable layout anchors."""

from __future__ import annotations

import pytest

from conftest import MAIN_PDF, REFERENCE_PDF, find_line_containing, line_center


ALIGNMENT_CASES = [
    {"id": "toc-title", "template_page": 8, "reference_page": 10, "phrase": "摘要", "x_tol": 8, "y_tol": 18},
    {"id": "lists-title", "template_page": 10, "reference_page": 12, "phrase": "图清单", "x_tol": 8, "y_tol": 18},
    {"id": "lists-subtitle", "template_page": 10, "reference_page": 12, "phrase": "表清单", "x_tol": 8, "y_tol": 48},
    {"id": "variables-title", "template_page": 11, "reference_page": 13, "phrase": "变量注释表", "x_tol": 8, "y_tol": 18},
    {"id": "variables-first-item", "template_page": 11, "reference_page": 13, "phrase": "V1", "x_tol": 25, "y_tol": 20},
    {"id": "originality-body", "template_page": 18, "reference_page": 21, "phrase": "除文中已经标明引用的内容外", "x_tol": 12, "y_tol": 24},
    {"id": "dataset-first-field", "template_page": 19, "reference_page": 22, "phrase": "关键词*", "x_tol": 40, "y_tol": 35},
    {"id": "dataset-org-field", "template_page": 19, "reference_page": 22, "phrase": "学位授予单位名称", "x_tol": 45, "y_tol": 60}
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
