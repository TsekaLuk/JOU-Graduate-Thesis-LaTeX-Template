#!/usr/bin/env python3
"""
研究生模板环境一致性检查脚本。
"""

from __future__ import annotations

import platform
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class EnvironmentChecker:
    def __init__(self) -> None:
        self.system = platform.system()
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.checks_passed = 0
        self.checks_total = 0

    def check_command(self, command: str, version_args: list[str] | None = None) -> bool:
        args = [command] + (version_args if version_args is not None else ["--version"])
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=5)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
        return result.returncode == 0

    def check_texlive_package(self, package: str) -> bool:
        for suffix in ("sty", "cls"):
            try:
                result = subprocess.run(
                    ["kpsewhich", f"{package}.{suffix}"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return False
            if result.returncode == 0 and result.stdout.strip():
                return True
        return False

    def check_item(self, label: str, ok: bool, *, critical: bool = True) -> None:
        self.checks_total += 1
        if ok:
            self.checks_passed += 1
            print(f"✓ {label}")
            return
        if critical:
            self.failures.append(label)
            print(f"✗ {label}")
        else:
            self.warnings.append(label)
            print(f"! {label}")

    def run(self) -> int:
        print("==> 研究生模板环境检查")
        print(f"操作系统: {self.system} {platform.release()}")
        print(f"Python 版本: {platform.python_version()}")

        print("\n==> 核心工具")
        for command, critical, version_args in (
            ("xelatex", True, None),
            ("bibtex", True, None),
            ("latexmk", False, None),
            ("pdftoppm", False, ["-v"]),
            ("pdftotext", False, ["-v"]),
            ("pdfinfo", False, ["-v"]),
        ):
            self.check_item(command, self.check_command(command, version_args), critical=critical)

        print("\n==> TeX Live 包")
        for package in (
            "ctex",
            "fontspec",
            "geometry",
            "fancyhdr",
            "titletoc",
            "graphicx",
            "natbib",
            "longtable",
            "caption",
            "booktabs",
            "tikz",
            "pgfplots",
            "textpos",
            "listings",
        ):
            self.check_item(f"包: {package}", self.check_texlive_package(package))

        print("\n==> 仓库关键文件")
        for path in (
            PROJECT_ROOT / "styles" / "jougraduate.cls",
            PROJECT_ROOT / "styles" / "joufonts.sty",
            PROJECT_ROOT / "references" / "江苏海洋大学研究生硕士学位论文撰写模版.pdf",
            PROJECT_ROOT / "contents" / "setup.tex",
            PROJECT_ROOT / "contents" / "user" / "frontmatter-content.tex",
            PROJECT_ROOT / "contents" / "user" / "chapters" / "01-introduction.tex",
        ):
            self.check_item(str(path.relative_to(PROJECT_ROOT)), path.exists())

        print("\n==> 开源字体")
        for path in (
            PROJECT_ROOT / "fonts" / "opensource" / "Tinos-Regular.ttf",
            PROJECT_ROOT / "fonts" / "opensource" / "NotoSerifCJKsc-Regular.otf",
            PROJECT_ROOT / "fonts" / "opensource" / "LXGWWenKaiGB-Regular.ttf",
        ):
            self.check_item(str(path.relative_to(PROJECT_ROOT)), path.exists(), critical=False)

        print("\n==> 总结")
        print(f"通过: {self.checks_passed}/{self.checks_total}")
        print(f"失败: {len(self.failures)}")
        print(f"警告: {len(self.warnings)}")
        if self.failures:
            print("需要先修复严重问题后再继续。")
            return 1
        if self.warnings:
            print("核心功能正常，但有可选增强项缺失。")
        else:
            print("环境检查通过。")
        return 0


def main() -> int:
    return EnvironmentChecker().run()


if __name__ == "__main__":
    sys.exit(main())
