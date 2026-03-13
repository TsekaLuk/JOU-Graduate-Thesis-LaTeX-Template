#!/usr/bin/env python3
"""Repository workflow and onboarding contracts."""

from __future__ import annotations

from conftest import (
    BODY_SAMPLE_PDF,
    CHECK_ENVIRONMENT_SCRIPT,
    GENERATE_COVER_DIFF_SCRIPT,
    GENERATE_README_IMAGES_SCRIPT,
    IMPORT_FONTS_SCRIPT,
    MAIN_FILE,
    NEW_CHAPTER_SCRIPT,
    PACKAGE_SCRIPT,
    PROJECT_ROOT,
    README_ASSET_DIR,
    README_FILE,
    README_IMAGE_DIR,
    USAGE_GUIDE,
)


def test_readme_contains_onboarding_sections():
    content = README_FILE.read_text(encoding="utf-8")
    for marker in [
        "## 发布渠道",
        "## 核心特性",
        "## 预览",
        "## 模板范围",
        "## 首次使用 60 秒",
        "## 本地编译（推荐）",
        "## AI 工具辅助写作",
        "## Overleaf（辅助预览，有限制）",
        "## QA",
    ]:
        assert marker in content, f"README 缺少 onboarding 章节: {marker}"


def test_readme_references_generated_preview_assets():
    content = README_FILE.read_text(encoding="utf-8")
    for marker in [
        "docs/images/cover-compare.png",
        "docs/images/abstract-compare.png",
        "docs/images/body-compare.png",
        "docs/images/thesis-gallery.png",
    ]:
        assert marker in content, f"README 缺少预览图引用: {marker}"


def test_usage_guide_exists():
    assert USAGE_GUIDE.exists(), "缺少 docs/guides/usage.md"


def test_makefile_workflow_targets_exist():
    content = (PROJECT_ROOT / "Makefile").read_text(encoding="utf-8")
    for marker in [
        "body-sample.pdf",
        "cover-diff:",
        "readme-images:",
        "env-check:",
        "doctor:",
        "quickstart:",
        "new-chapter:",
        "package:",
    ]:
        assert marker in content, f"Makefile 缺少目标: {marker}"


def test_support_scripts_exist():
    for path in [
        IMPORT_FONTS_SCRIPT,
        NEW_CHAPTER_SCRIPT,
        CHECK_ENVIRONMENT_SCRIPT,
        GENERATE_COVER_DIFF_SCRIPT,
        GENERATE_README_IMAGES_SCRIPT,
        PACKAGE_SCRIPT,
    ]:
        assert path.exists(), f"缺少脚本: {path.name}"


def test_package_script_is_graduate_specific():
    content = PACKAGE_SCRIPT.read_text(encoding="utf-8")
    assert "ProvidesClass{jougraduate}" in content
    assert "JOU 研究生论文模板打包脚本" in content
    assert "jougraduate-overleaf-gallery" in content
    assert "jougraduate-overleaf" in content
    assert "jougraduate-ctan" in content
    for forbidden in [
        "ProvidesClass{jouthesis}",
        "README_EN.md",
        "JOU Undergraduate Thesis",
        "18 supplementary templates",
        "contents/acknowledgements.tex",
    ]:
        assert forbidden not in content, f"打包脚本仍残留本科或错误路径: {forbidden}"


def test_body_sample_file_exists_and_is_wired():
    sample_tex = PROJECT_ROOT / "samples" / "body-sample.tex"
    content = sample_tex.read_text(encoding="utf-8")
    assert sample_tex.exists(), "缺少正文样页样本文件"
    assert "\\input{contents/samples/body-sample-content}" in content
    assert "\\input{contents/chapters/chapter1}" in content
    assert "\\input{contents/chapters/chapter1-sample}" in content
    assert BODY_SAMPLE_PDF.exists(), "缺少编译后的正文样页 PDF"


def test_preview_assets_exist():
    expected_paths = [
        README_IMAGE_DIR / "cover-compare.png",
        README_IMAGE_DIR / "abstract-compare.png",
        README_IMAGE_DIR / "body-compare.png",
        README_IMAGE_DIR / "thesis-gallery.png",
        README_ASSET_DIR / "graduate-cover-overlay.png",
        README_ASSET_DIR / "graduate-cover-diff.png",
        README_ASSET_DIR / "graduate-cover-checker.png",
    ]
    for path in expected_paths:
        assert path.exists(), f"缺少预览资产: {path.relative_to(PROJECT_ROOT)}"
        assert path.stat().st_size > 0, f"预览资产为空: {path.relative_to(PROJECT_ROOT)}"


def test_main_inputs_shared_content_layer():
    content = MAIN_FILE.read_text(encoding="utf-8")
    assert "\\input{contents/setup}" in content
    assert "\\input{contents/shared/thesis-content}" in content


def test_repository_exposes_setup_and_user_chapters():
    assert (PROJECT_ROOT / "contents" / "setup.tex").exists(), "缺少集中配置入口 setup.tex"
    assert (PROJECT_ROOT / "contents" / "user" / "chapters" / "01-introduction.tex").exists(), "缺少用户章节示例"
    assert (PROJECT_ROOT / "contents" / "user" / "chapters" / "_template.tex").exists(), "缺少章节模板文件"
    assert (PROJECT_ROOT / "contents" / "user" / "chapters" / "README.md").exists(), "缺少章节目录说明"
    assert (PROJECT_ROOT / ".latexmkrc").exists(), "缺少本地 latexmk 配置文件"
    assert (PROJECT_ROOT / "build.bat").exists(), "缺少 Windows 构建脚本"


def test_readme_mentions_page_switches_and_windows_build():
    content = README_FILE.read_text(encoding="utf-8")
    for marker in [
        "## 页面开关",
        "blind-review",
        "include-appendix",
        "build.bat",
        "contents/user/chapters/_template.tex",
        "make new-chapter",
        "make quickstart",
        "make doctor",
    ]:
        assert marker in content, f"README 缺少新的 UX 指引: {marker}"


def test_readme_contains_cross_platform_consistency_guide():
    content = README_FILE.read_text(encoding="utf-8")
    for marker in [
        "## 跨系统一致性指南",
        "make import-fonts",
        "make env-check",
        "make doctor",
        "make",
        "字体不一致时，常见差异包括：",
        "命中同一套正式字体：跨系统结果通常会很接近",
        "一台机器走正式字体、一台机器走开源兜底字体：通常仍能正常编译，但版式可能有轻微差异",
    ]:
        assert marker in content, f"README 缺少跨系统一致性说明: {marker}"


def test_usage_guide_mentions_quickstart_and_doctor():
    content = USAGE_GUIDE.read_text(encoding="utf-8")
    for marker in [
        "## 第一次打开仓库先做什么",
        "make quickstart",
        "make doctor",
        "## 常见任务",
    ]:
        assert marker in content, f"使用指南缺少 UX 入口: {marker}"


def test_new_chapter_script_supports_dry_run():
    import subprocess

    completed = subprocess.run(
        [
            "python3",
            str(NEW_CHAPTER_SCRIPT),
            "--name",
            "08-literature-review",
            "--title-cn",
            "文献综述",
            "--title-en",
            "Literature Review",
            "--dry-run",
        ],
        cwd=PROJECT_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    output = completed.stdout
    assert "08-literature-review.tex" in output
    assert "contents/chapters/mainmatter.tex" in output
