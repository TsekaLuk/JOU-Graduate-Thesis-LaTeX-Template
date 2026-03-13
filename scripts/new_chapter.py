#!/usr/bin/env python3
"""Scaffold a new user chapter and wire it into mainmatter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = PROJECT_ROOT / "contents" / "user" / "chapters" / "_template.tex"
CHAPTER_DIR = PROJECT_ROOT / "contents" / "user" / "chapters"
MAINMATTER_PATH = PROJECT_ROOT / "contents" / "chapters" / "mainmatter.tex"


def normalize_name(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError("章节文件名不能为空")
    if not name.endswith(".tex"):
        name = f"{name}.tex"
    if "/" in name or "\\" in name:
        raise ValueError("章节文件名只能是文件名，不能包含目录")
    return name


def chapter_label(name: str) -> str:
    stem = Path(name).stem
    return "chap:" + re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()


def render_template(name: str, title_cn: str, title_en: str) -> str:
    content = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{中文章节标题}": "{" + title_cn + "}",
        "{English Chapter Title}": "{" + title_en + "}",
        "{chap:your-chapter}": "{" + chapter_label(name) + "}",
        "{中文小节标题}": "{研究内容}",
        "{English Section Title}": "{Research Scope}",
        "{三级标题}": "{研究问题}",
    }
    for source, target in replacements.items():
        content = content.replace(source, target)
    return content


def update_mainmatter(name: str, *, dry_run: bool) -> bool:
    desired = f"\\input{{contents/user/chapters/{Path(name).stem}}}"
    lines = MAINMATTER_PATH.read_text(encoding="utf-8").splitlines()
    current_inputs = [line.strip() for line in lines if line.strip().startswith("\\input{contents/user/chapters/")]
    if desired in current_inputs:
        return False

    prefix_lines: list[str] = []
    for line in lines:
        if line.strip().startswith("\\input{contents/user/chapters/"):
            break
        prefix_lines.append(line)

    new_inputs = sorted(current_inputs + [desired])
    new_content = "\n".join(prefix_lines + new_inputs) + "\n"
    if not dry_run:
        MAINMATTER_PATH.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="为研究生论文模板新增一个正文章节。")
    parser.add_argument("--name", required=True, help="章节文件名，例如 08-literature-review 或 08-literature-review.tex")
    parser.add_argument("--title-cn", required=True, help="中文章节标题")
    parser.add_argument("--title-en", required=True, help="英文章节标题")
    parser.add_argument("--dry-run", action="store_true", help="只预览将要创建/修改的内容，不实际写文件")
    args = parser.parse_args()

    try:
        name = normalize_name(args.name)
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 2

    target = CHAPTER_DIR / name
    if target.exists():
        print(f"错误: 章节文件已存在: {target}", file=sys.stderr)
        return 2

    rendered = render_template(name, args.title_cn, args.title_en)

    if args.dry_run:
        print(f"[dry-run] 将创建: {target.relative_to(PROJECT_ROOT)}")
        print(f"[dry-run] 将接入: {MAINMATTER_PATH.relative_to(PROJECT_ROOT)}")
        print("")
        print(rendered)
        return 0

    target.write_text(rendered, encoding="utf-8")
    mainmatter_changed = update_mainmatter(name, dry_run=False)

    print(f"已创建章节: {target.relative_to(PROJECT_ROOT)}")
    if mainmatter_changed:
        print(f"已更新正文入口: {MAINMATTER_PATH.relative_to(PROJECT_ROOT)}")
    else:
        print("正文入口已包含该章节，无需更新")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
