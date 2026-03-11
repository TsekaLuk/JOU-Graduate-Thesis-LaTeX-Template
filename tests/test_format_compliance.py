#!/usr/bin/env python3
"""Static format and repository-contract checks for the graduate template."""

from __future__ import annotations

from conftest import CLASS_FILE, HEADINGS_FILE, MAIN_FILE, PROJECT_ROOT


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
        "学位授予单位名称",
        "学位授予单位代",
        "论文题名",
        "作者姓名",
        "导师姓名",
    ]:
        assert marker in dataset, f"数据集页面缺少字段: {marker}"


def test_user_editable_content_is_externalized():
    content_file = PROJECT_ROOT / "contents" / "shared" / "thesis-content.tex"
    assert content_file.exists(), "缺少统一内容入口 thesis-content.tex"

    content = content_file.read_text(encoding="utf-8")
    for marker in [
        "\\input{contents/user/frontmatter-content}",
        "\\input{contents/user/body-content}",
        "\\input{contents/user/backmatter-content}",
    ]:
        assert marker in content, f"内容入口未聚合用户内容文件: {marker}"

    frontmatter_content = (PROJECT_ROOT / "contents" / "user" / "frontmatter-content.tex").read_text(encoding="utf-8")
    body_content = (PROJECT_ROOT / "contents" / "user" / "body-content.tex").read_text(encoding="utf-8")
    backmatter_content = (PROJECT_ROOT / "contents" / "user" / "backmatter-content.tex").read_text(encoding="utf-8")
    for marker in ["JOUAcknowledgementsBody", "JOUCNAbstractBody", "JOUVariableRows"]:
        assert marker in frontmatter_content, f"前置内容文件缺少关键字段: {marker}"
    for marker in ["JOUBodyFirstParagraph", "JOUBodySecondTableRows", "JOUBodySecondFigureTitleEN"]:
        assert marker in body_content, f"正文内容文件缺少关键字段: {marker}"
    for marker in ["JOUAppendixProgramTitle", "JOUAuthorResumeBody", "JOUOriginalityStatementBody", "JOUDataCollectionFormatLine"]:
        assert marker in backmatter_content, f"后置内容文件缺少关键字段: {marker}"

    layout_files = {
        PROJECT_ROOT / "contents" / "frontmatter" / "acknowledgements.tex": "\\JOUAcknowledgementsBody",
        PROJECT_ROOT / "contents" / "frontmatter" / "cn-abstract.tex": "\\JOUCNAbstractBody",
        PROJECT_ROOT / "contents" / "frontmatter" / "en-abstract.tex": "\\JOUENAbstractBody",
        PROJECT_ROOT / "contents" / "frontmatter" / "variables.tex": "\\JOUVariableRows",
        PROJECT_ROOT / "contents" / "chapters" / "chapter1.tex": "\\JOUBodyFirstParagraph",
        PROJECT_ROOT / "contents" / "chapters" / "chapter1-sample.tex": "\\JOUBodySecondTableRows",
        PROJECT_ROOT / "contents" / "appendices" / "program.tex": "\\JOUAppendixProgramTitle",
        PROJECT_ROOT / "contents" / "backmatter" / "author-resume.tex": "\\JOUAuthorResumeBody",
        PROJECT_ROOT / "contents" / "backmatter" / "originality.tex": "\\JOUOriginalityStatementBody",
        PROJECT_ROOT / "contents" / "backmatter" / "dataset.tex": "\\JOUDataCollectionFormatLine",
    }
    for path, marker in layout_files.items():
        assert marker in path.read_text(encoding="utf-8"), f"{path.name} 仍未引用统一内容层"


def test_main_inputs_shared_content_layer():
    assert "\\input{contents/shared/thesis-content}" in MAIN_FILE.read_text(encoding="utf-8")


def test_body_pages_use_real_thesis_commands():
    chapter_file = (PROJECT_ROOT / "contents" / "chapters" / "chapter1.tex").read_text(encoding="utf-8")
    sample_file = (PROJECT_ROOT / "contents" / "chapters" / "chapter1-sample.tex").read_text(encoding="utf-8")
    toc_file = (PROJECT_ROOT / "contents" / "frontmatter" / "toc-cn.tex").read_text(encoding="utf-8")
    toc_en_file = (PROJECT_ROOT / "contents" / "frontmatter" / "toc-en.tex").read_text(encoding="utf-8")
    lists_file = (PROJECT_ROOT / "contents" / "frontmatter" / "lists.tex").read_text(encoding="utf-8")
    variables_file = (PROJECT_ROOT / "contents" / "frontmatter" / "variables.tex").read_text(encoding="utf-8")

    assert "\\JOUChapterWithEnglish" in chapter_file, "正文首页应使用中英文章节封装命令"
    assert "\\subsection{研究方法}" in sample_file, "正文示例页应使用正常三级标题命令"
    assert "\\JOUTableBicaption" in sample_file, "图表页应通过双语 caption 生成清单"
    assert "\\JOUFigureBicaption" in sample_file, "图表页应通过双语 caption 生成清单"
    assert "\\@starttoc{toc}" in toc_file, "中文目录应使用 LaTeX 自动目录链路"
    assert "\\@starttoc{toe}" in toc_en_file, "英文目录应使用独立自动目录链路"
    assert "\\@starttoc{lof}" in lists_file and "\\@starttoc{lot}" in lists_file, "图表清单应使用自动清单链路"
    assert "\\begin{longtable}" in variables_file, "变量表应使用正常 longtable 排版"
