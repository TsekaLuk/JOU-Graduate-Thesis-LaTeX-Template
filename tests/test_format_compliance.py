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
        "JOUSetup",
        "JOUApplySharedMetadata",
    ]:
        assert marker in content, f"jougraduate.cls 缺少关键格式标记: {marker}"


def test_headings_fix_toc_depth_and_header_text():
    content = HEADINGS_FILE.read_text(encoding="utf-8")
    assert "setcounter{tocdepth}{1}" in content, "目录深度应固定到二级标题"
    assert "江苏海洋大学硕士学位论文" in content, "页眉文本未切换到研究生模板"


def test_dataset_page_contains_required_fields(thesis_pages: dict[int, str]):
    dataset = thesis_pages[25]
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
        "\\input{contents/user/backmatter-content}",
    ]:
        assert marker in content, f"内容入口未聚合用户内容文件: {marker}"

    setup_content = (PROJECT_ROOT / "contents" / "setup.tex").read_text(encoding="utf-8")
    frontmatter_content = (PROJECT_ROOT / "contents" / "user" / "frontmatter-content.tex").read_text(encoding="utf-8")
    backmatter_content = (PROJECT_ROOT / "contents" / "user" / "backmatter-content.tex").read_text(encoding="utf-8")
    chapter_content = (PROJECT_ROOT / "contents" / "user" / "chapters" / "01-introduction.tex").read_text(encoding="utf-8")
    sample_content = (PROJECT_ROOT / "contents" / "samples" / "body-sample-content.tex").read_text(encoding="utf-8")
    for marker in ["\\JOUSetup{", "title-cn", "supervisor-name", "submission-date"]:
        assert marker in setup_content, f"集中配置入口缺少关键字段: {marker}"
    for marker in [
        "第 1 步：首次使用必改字段",
        "第 2 步：常用补充字段",
        "第 3 步：低频字段，通常按学院要求再改",
        "第 4 步：页面开关",
        "第 5 步：匿名评审",
    ]:
        assert marker in setup_content, f"setup.tex 缺少写作者友好的分区提示: {marker}"
    for marker in [
        "blind-review = false",
        "include-acknowledgements = true",
        "include-appendix = true",
        "include-author-resume = true",
        "include-originality = true",
        "include-dataset = true",
    ]:
        assert marker in setup_content, f"setup.tex 缺少页面开关: {marker}"
    for marker in ["JOUAcknowledgementsBody", "JOUCNAbstractBody", "JOUVariableRows"]:
        assert marker in frontmatter_content, f"前置内容文件缺少关键字段: {marker}"
    for marker in ["\\JOUChapterWithEnglish", "\\JOUTableBicaption", "\\JOUFigureBicaption"]:
        assert marker in chapter_content, f"正文写作章节缺少关键结构: {marker}"
    for marker in ["JOUChapterOneOpeningParagraph", "JOUBodySecondTableRows", "JOUBodySecondFigureTitleEN"]:
        assert marker in sample_content, f"正文样页数据层缺少关键字段: {marker}"
    for marker in ["JOUConclusionBody", "JOUAppendixProgramTitle", "JOUAuthorResumeBody", "JOUOriginalityStatementBody", "JOUDataCollectionFormatLine"]:
        assert marker in backmatter_content, f"后置内容文件缺少关键字段: {marker}"

    layout_files = {
        PROJECT_ROOT / "contents" / "frontmatter" / "acknowledgements.tex": "\\JOUAcknowledgementsBody",
        PROJECT_ROOT / "contents" / "frontmatter" / "cn-abstract.tex": "\\JOUCNAbstractBody",
        PROJECT_ROOT / "contents" / "frontmatter" / "en-abstract.tex": "\\JOUENAbstractBody",
        PROJECT_ROOT / "contents" / "frontmatter" / "variables.tex": "\\JOUVariableRows",
        PROJECT_ROOT / "contents" / "chapters" / "chapter1.tex": "\\JOUChapterOneOpeningParagraph",
        PROJECT_ROOT / "contents" / "chapters" / "chapter1-sample.tex": "\\JOUBodySecondTableRows",
        PROJECT_ROOT / "contents" / "backmatter" / "conclusion.tex": "\\JOUConclusionBody",
        PROJECT_ROOT / "contents" / "appendices" / "program.tex": "\\JOUAppendixProgramTitle",
        PROJECT_ROOT / "contents" / "backmatter" / "author-resume.tex": "\\JOUAuthorResumeBody",
        PROJECT_ROOT / "contents" / "backmatter" / "originality.tex": "\\JOUOriginalityStatementBody",
        PROJECT_ROOT / "contents" / "backmatter" / "dataset.tex": "\\JOUDataCollectionFormatLine",
    }
    for path, marker in layout_files.items():
        assert marker in path.read_text(encoding="utf-8"), f"{path.name} 仍未引用统一内容层"


def test_main_inputs_shared_content_layer():
    content = MAIN_FILE.read_text(encoding="utf-8")
    assert "\\input{contents/setup}" in content
    assert "\\input{contents/shared/thesis-content}" in content
    assert "\\input{contents/chapters/mainmatter}" in content
    for marker in [
        "\\ifJOUBlindReview",
        "\\ifJOUIncludeAcknowledgements",
        "\\ifJOUIncludeAppendix",
        "\\ifJOUIncludeAuthorResume",
        "\\ifJOUIncludeOriginality",
        "\\ifJOUIncludeDataset",
    ]:
        assert marker in content, f"main.tex 缺少页面开关逻辑: {marker}"


def test_body_pages_use_real_thesis_commands():
    chapter_file = (PROJECT_ROOT / "contents" / "user" / "chapters" / "01-introduction.tex").read_text(encoding="utf-8")
    sample_file = (PROJECT_ROOT / "contents" / "chapters" / "chapter1-sample.tex").read_text(encoding="utf-8")
    mainmatter_file = (PROJECT_ROOT / "contents" / "chapters" / "mainmatter.tex").read_text(encoding="utf-8")
    toc_file = (PROJECT_ROOT / "contents" / "frontmatter" / "toc-cn.tex").read_text(encoding="utf-8")
    toc_en_file = (PROJECT_ROOT / "contents" / "frontmatter" / "toc-en.tex").read_text(encoding="utf-8")
    lists_file = (PROJECT_ROOT / "contents" / "frontmatter" / "lists.tex").read_text(encoding="utf-8")
    variables_file = (PROJECT_ROOT / "contents" / "frontmatter" / "variables.tex").read_text(encoding="utf-8")
    en_abstract_file = (PROJECT_ROOT / "contents" / "frontmatter" / "en-abstract.tex").read_text(encoding="utf-8")

    assert "\\JOUChapterWithEnglish" in chapter_file, "正文首页应使用中英文章节封装命令"
    assert "\\subsection{研究方法}" in chapter_file, "正文主写作章节应包含真实的三级标题"
    assert "\\input{contents/user/chapters/01-introduction}" in mainmatter_file, "正文聚合入口应引用用户章节文件"
    assert "\\subsection{\\JOUBodySecondSubsectionTitle}" in sample_file, "正文示例页应继续使用样页数据层驱动的三级标题"
    assert "\\JOUAuthorDisplay" in (PROJECT_ROOT / "contents" / "frontmatter" / "cover.tex").read_text(encoding="utf-8"), "封面应通过盲审显示宏输出作者信息"
    assert "\\JOUCollegeDisplay" in (PROJECT_ROOT / "contents" / "frontmatter" / "inner-cover.tex").read_text(encoding="utf-8"), "内封应通过盲审显示宏输出培养单位"
    dataset_file = (PROJECT_ROOT / "contents" / "backmatter" / "dataset.tex").read_text(encoding="utf-8")
    for marker in ["\\JOUStudentIdDisplay", "\\JOUTrainingUnitNameDisplay", "\\JOUSupervisorNameDisplay", "\\JOUReviewersDisplay"]:
        assert marker in dataset_file, f"数据集页缺少盲审显示宏: {marker}"
    assert "\\JOUTableBicaption" in sample_file, "图表页应通过双语 caption 生成清单"
    assert "\\JOUFigureBicaption" in sample_file, "图表页应通过双语 caption 生成清单"
    assert "\\@starttoc{toc}" in toc_file, "中文目录应使用 LaTeX 自动目录链路"
    assert "\\@starttoc{toe}" in toc_en_file, "英文目录应使用独立自动目录链路"
    assert "\\@starttoc{lof}" in lists_file and "\\@starttoc{lot}" in lists_file, "图表清单应使用自动清单链路"
    assert "\\begin{longtable}" in variables_file, "变量表应使用正常 longtable 排版"
    assert "\\addcontentsline{toc}{chapter}{Abstract}" not in en_abstract_file, "英文摘要不应写入中文目录"


def test_backmatter_pages_do_not_bleed_next_page_titles():
    appendix_file = (PROJECT_ROOT / "contents" / "appendices" / "program.tex").read_text(encoding="utf-8")
    resume_file = (PROJECT_ROOT / "contents" / "backmatter" / "author-resume.tex").read_text(encoding="utf-8")
    originality_file = (PROJECT_ROOT / "contents" / "backmatter" / "originality.tex").read_text(encoding="utf-8")
    conclusion_file = (PROJECT_ROOT / "contents" / "backmatter" / "conclusion.tex").read_text(encoding="utf-8")

    assert "作者简历" not in appendix_file, "附录页不应提前硬编码下一页标题"
    assert "学位论文原创性声明" not in resume_file, "作者简历页不应提前硬编码下一页标题"
    assert "\\JOUDataCollectionStartTitle" not in originality_file, "原创性声明页不应提前硬编码数据集标题"
    assert "\\setcounter{chapter}" not in conclusion_file, "结论页不应通过硬编码章节计数伪造编号"


def test_narrative_content_avoids_manual_line_break_hardcoding():
    frontmatter_content = (PROJECT_ROOT / "contents" / "user" / "frontmatter-content.tex").read_text(encoding="utf-8")
    chapter_content = (PROJECT_ROOT / "contents" / "user" / "chapters" / "01-introduction.tex").read_text(encoding="utf-8")
    backmatter_content = (PROJECT_ROOT / "contents" / "user" / "backmatter-content.tex").read_text(encoding="utf-8")

    assert "method and\\\\" not in frontmatter_content, "英文摘要正文不应依赖手工换行"
    assert "柱的旋流场结构，分析旋流场特征及其影响；借助\\\\" not in chapter_content, "正文叙述段落不应依赖手工换行"
    assert "application/msword;\\allowbreak application/pdf" in backmatter_content, "数据集推荐格式应允许自动换行"
