#!/usr/bin/env python3
"""Page ordering and anchor contract for the graduate thesis template."""

from __future__ import annotations

import pytest

from conftest import MAIN_PDF, find_page_by_phrases, pdf_page_count


@pytest.mark.parametrize("page_case", [*__import__("json").loads(__import__("pathlib").Path(__file__).with_name("graduate_reference_spec.json").read_text(encoding="utf-8"))["pages"]], ids=lambda case: case["id"])
def test_page_anchor_maps_to_expected_page(thesis_pages: dict[int, str], page_case: dict):
    found = find_page_by_phrases(thesis_pages, page_case["phrases"])
    assert found is not None, f"[{page_case['id']}] 未找到页面锚点"
    assert found == page_case["template_page"], f"[{page_case['id']}] 当前位于第 {found} 页，预期第 {page_case['template_page']} 页"


def test_pages_are_in_strict_order(reference_spec: dict, thesis_pages: dict[int, str]):
    found_pages = []
    for page_case in reference_spec["pages"]:
        found = find_page_by_phrases(thesis_pages, page_case["phrases"])
        assert found is not None, f"[{page_case['id']}] 未找到页面锚点"
        found_pages.append(found)
    assert found_pages == sorted(found_pages), "研究生论文页面顺序发生回退"


def test_extended_abstract_not_generated(thesis_pages: dict[int, str]):
    assert all("ExtendedAbstract" not in text for text in thesis_pages.values()), "硕士模板默认不应生成 Extended Abstract"


def test_main_pdf_page_count_matches_contract():
    assert pdf_page_count(MAIN_PDF) == 25, "主模板页数不符合当前研究生对齐合同"


def test_combined_lists_page_present(thesis_pages: dict[int, str]):
    lists_page = find_page_by_phrases(thesis_pages, ["图清单", "表清单", "Particlesizedistributionresults"])
    assert lists_page == 10, "图清单/表清单应位于同一页且固定在第 10 页"


def test_chinese_toc_excludes_english_abstract(thesis_pages: dict[int, str]):
    toc_cn = thesis_pages[8]
    assert "Abstract" not in toc_cn, "中文目录不应包含英文摘要条目"


def test_english_toc_still_contains_english_abstract(thesis_pages: dict[int, str]):
    toc_en = thesis_pages[9]
    assert "Abstract" in toc_en, "英文目录应包含英文摘要条目"
