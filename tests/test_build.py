#!/usr/bin/env python3
"""Basic build regression checks for the graduate thesis template."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import pytest

from conftest import BODY_SAMPLE_PDF, MAIN_PDF, PROJECT_ROOT, normalize, page_text, pdf_page_count, pdffonts


# ── Build output ────────────────────────────────────────────────────────────

def test_main_pdf_exists():
    assert MAIN_PDF.exists(), "缺少 main.pdf，论文未成功编译"


def test_main_pdf_is_nonempty():
    assert MAIN_PDF.stat().st_size > 1024, "main.pdf 体积异常（< 1 KB），疑似空文件"


def test_main_pdf_page_count():
    assert pdf_page_count(MAIN_PDF) == 25, "当前主模板页数与研究生论文合同不一致"


def test_body_sample_pdf_exists():
    assert BODY_SAMPLE_PDF.exists(), "缺少 body-sample.pdf，正文样页基线未成功编译"


def test_body_sample_pdf_is_nonempty():
    assert BODY_SAMPLE_PDF.stat().st_size > 1024, "body-sample.pdf 体积异常（< 1 KB），疑似空文件"


def test_body_sample_pdf_page_count():
    assert pdf_page_count(BODY_SAMPLE_PDF) == 2, "正文样页基线页数应固定为 2 页"


def test_main_build_log_has_no_box_warnings():
    log_path = Path("main.log")
    assert log_path.exists(), "缺少 main.log，无法检查版式告警"
    log_text = log_path.read_text(encoding="utf-8", errors="ignore")
    assert "Overfull \\hbox" not in log_text, "main.log 仍存在 Overfull \\hbox，说明模板仍在靠硬撑布局"
    assert "Underfull \\hbox" not in log_text, "main.log 仍存在 Underfull \\hbox，说明模板仍在靠手工换行或空格撑版"


# ── Font stack ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def fonts_output() -> str:
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    return pdffonts(MAIN_PDF)


def test_pdf_has_embedded_fonts(fonts_output: str):
    non_header_lines = [l for l in fonts_output.splitlines() if l.strip() and "name" not in l.lower()]
    assert len(non_header_lines) > 0, "main.pdf 未嵌入任何字体，PDF 可能为空或编译异常。"


@pytest.fixture(scope="module")
def blind_review_sample() -> dict[str, object]:
    with tempfile.TemporaryDirectory(dir=PROJECT_ROOT) as temp_dir:
        temp_path = Path(temp_dir)
        tex_path = PROJECT_ROOT / "blind-review-check-temp.tex"
        tex_path.write_text(
            r"""\documentclass{styles/jougraduate}
\input{contents/setup}
\input{contents/shared/thesis-content}
\JOUApplySharedMetadata
\JOUSetup{blind-review = true}
\begin{document}
\input{contents/frontmatter/cover}
\input{contents/frontmatter/inner-cover}
\frontmatter
\setcounter{page}{1}
\pagenumbering{Roman}
\pagestyle{frontmatterstyle}
\input{contents/backmatter/dataset}
\end{document}
""",
            encoding="utf-8",
        )
        try:
            for _ in range(2):
                subprocess.run(
                    [
                        "xelatex",
                        "-interaction=nonstopmode",
                        "-halt-on-error",
                        f"-output-directory={temp_path}",
                        tex_path.name,
                    ],
                    cwd=PROJECT_ROOT,
                    check=True,
                    text=True,
                    capture_output=True,
                )
            pdf_path = temp_path / "blind-review-check-temp.pdf"
            return {
                "count": pdf_page_count(pdf_path),
                "pages": {page: normalize(page_text(pdf_path, page)) for page in range(1, pdf_page_count(pdf_path) + 1)},
            }
        finally:
            tex_path.unlink(missing_ok=True)


def test_blind_review_sample_masks_personal_fields(blind_review_sample: dict[str, object]):
    assert blind_review_sample["count"] == 3, "盲审样本应只编译封面、内封和数据集三页"
    pages = blind_review_sample["pages"]
    assert "匿名" in pages[1], "盲审封面应隐藏作者或导师姓名"
    assert "***" not in pages[1], "盲审封面不应暴露原始作者占位内容"
    assert "化工学院" not in pages[2], "盲审内封不应暴露培养单位"
    assert "隐去" in pages[2], "盲审内封应使用匿名占位"
    assert "2023123456" not in pages[3], "盲审数据集不应暴露学号"
    assert "江苏省连云港市" not in pages[3], "盲审数据集不应暴露培养单位地址"
