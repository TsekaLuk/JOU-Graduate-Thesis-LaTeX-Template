"""Shared fixtures and helpers for the JOU graduate thesis template test suite."""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

import pytest
from PIL import Image


# ── Path constants ──────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAIN_PDF = PROJECT_ROOT / "main.pdf"
BODY_SAMPLE_PDF = PROJECT_ROOT / "body-sample.pdf"
MAIN_FILE = PROJECT_ROOT / "main.tex"
CLASS_FILE = PROJECT_ROOT / "styles" / "jougraduate.cls"
HEADINGS_FILE = PROJECT_ROOT / "styles" / "jougraduateheadings.sty"
JOUFONTS_FILE = PROJECT_ROOT / "styles" / "joufonts.sty"
FONT_DIR = PROJECT_ROOT / "fonts" / "opensource"
REFERENCE_DOC = PROJECT_ROOT / "references" / "江苏海洋大学研究生硕士学位论文撰写模版.doc"
REFERENCE_DOCX = PROJECT_ROOT / "references" / "江苏海洋大学研究生硕士学位论文撰写模版.docx"
REFERENCE_PDF = PROJECT_ROOT / "references" / "江苏海洋大学研究生硕士学位论文撰写模版.pdf"
REFERENCE_XML = PROJECT_ROOT / "references" / "unpacked" / "word" / "document.xml"
SPEC_PATH = PROJECT_ROOT / "tests" / "graduate_reference_spec.json"
CHECK_FONTS_SCRIPT = PROJECT_ROOT / "scripts" / "check_fonts.py"
CHECK_ENVIRONMENT_SCRIPT = PROJECT_ROOT / "scripts" / "check_environment.py"
IMPORT_FONTS_SCRIPT = PROJECT_ROOT / "scripts" / "import_fonts.py"
NEW_CHAPTER_SCRIPT = PROJECT_ROOT / "scripts" / "new_chapter.py"
PACKAGE_SCRIPT = PROJECT_ROOT / "scripts" / "package_for_distribution.sh"
GENERATE_COVER_DIFF_SCRIPT = PROJECT_ROOT / "scripts" / "generate_cover_diff.py"
GENERATE_README_IMAGES_SCRIPT = PROJECT_ROOT / "scripts" / "generate_readme_images.py"
README_FILE = PROJECT_ROOT / "README.md"
USAGE_GUIDE = PROJECT_ROOT / "docs" / "guides" / "usage.md"
README_IMAGE_DIR = PROJECT_ROOT / "docs" / "images"
README_ASSET_DIR = PROJECT_ROOT / "docs" / "assets"
WORKFLOW_FILE = PROJECT_ROOT / ".github" / "workflows" / "cross-platform-fonts.yml"
FONTPATHS_EXAMPLE = PROJECT_ROOT / "styles" / "joufontspaths.local.example.tex"

RENDER_DPI = 160


# ── Utility functions ───────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Collapse all whitespace (including CJK ideographic space) for comparison."""
    text = text.replace("\u3000", " ")
    return re.sub(r"\s+", "", text)


def page_text(pdf: Path, page: int) -> str:
    """Extract the raw text of a single PDF page via pdftotext."""
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def pdf_page_count(pdf: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(pdf)],
        check=True,
        text=True,
        capture_output=True,
    )
    match = re.search(r"^Pages:\s+(\d+)$", completed.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError("无法从 pdfinfo 输出解析页数")
    return int(match.group(1))


def pdffonts(pdf: Path) -> str:
    completed = subprocess.run(
        ["pdffonts", str(pdf)],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout


def render_page(pdf: Path, page: int, *, dpi: int = RENDER_DPI) -> Image.Image:
    """Render a single PDF page to a greyscale PIL Image."""
    with tempfile.TemporaryDirectory() as temp_dir:
        prefix = Path(temp_dir) / "page"
        subprocess.run(
            [
                "pdftoppm",
                "-f", str(page),
                "-l", str(page),
                "-r", str(dpi),
                "-png",
                str(pdf),
                str(prefix),
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        candidates = sorted(Path(temp_dir).glob("page-*.png"))
        if not candidates:
            raise RuntimeError(f"无法渲染 {pdf.name} 第 {page} 页为 PNG")
        return Image.open(candidates[0]).convert("L").copy()


def get_pdfinfo(pdf_path: Path) -> dict[str, str]:
    info_text = subprocess.run(
        ["pdfinfo", str(pdf_path)], check=True, text=True, capture_output=True,
    ).stdout
    info: dict[str, str] = {}
    for line in info_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


def bbox_lines(pdf: Path, page: int) -> list[dict[str, float | str]]:
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-bbox-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True,
        text=True,
        capture_output=True,
    )
    html = completed.stdout
    line_pattern = re.compile(
        r'<line xMin="(?P<xmin>[^"]+)" yMin="(?P<ymin>[^"]+)" '
        r'xMax="(?P<xmax>[^"]+)" yMax="(?P<ymax>[^"]+)">(?P<body>.*?)</line>',
        re.DOTALL,
    )
    word_pattern = re.compile(r"<word [^>]*>(?P<text>.*?)</word>", re.DOTALL)

    lines: list[dict[str, float | str]] = []
    for match in line_pattern.finditer(html):
        words = "".join(word_pattern.findall(match.group("body")))
        lines.append(
            {
                "text": words,
                "xMin": float(match.group("xmin")),
                "yMin": float(match.group("ymin")),
                "xMax": float(match.group("xmax")),
                "yMax": float(match.group("ymax")),
            }
        )
    return lines


def find_line_containing(pdf: Path, page: int, pattern: str) -> dict[str, float | str] | None:
    normalized_pattern = normalize(pattern)
    candidates: list[dict[str, float | str]] = []
    for line in bbox_lines(pdf, page):
        normalized_text = normalize(str(line["text"]))
        if normalized_pattern == normalized_text:
            return line
        if normalized_pattern in normalized_text or normalized_text in normalized_pattern:
            candidates.append(line)
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda item: (
            abs(len(normalize(str(item["text"]))) - len(normalized_pattern)),
            float(item["yMin"]),
            float(item["xMin"]),
        ),
    )


def line_center(line: dict[str, float | str]) -> tuple[float, float]:
    return (
        (float(line["xMin"]) + float(line["xMax"])) / 2,
        (float(line["yMin"]) + float(line["yMax"])) / 2,
    )


def find_page_by_phrases(pages: dict[int, str], phrases: list[str]) -> int | None:
    normalized_phrases = [normalize(p) for p in phrases]
    for page, text in pages.items():
        if all(phrase in text for phrase in normalized_phrases):
            return page
    return None


@pytest.fixture(scope="session")
def reference_spec() -> dict:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def thesis_pages() -> dict[int, str]:
    if not MAIN_PDF.exists():
        pytest.skip("缺少 main.pdf")
    return {page: normalize(page_text(MAIN_PDF, page)) for page in range(1, pdf_page_count(MAIN_PDF) + 1)}
