#!/usr/bin/env python3
"""
一键导入研究生论文模板所需的标准字体到 fonts/proprietary/。

优先从常见系统目录、WPS 安装目录和桌面字体目录中查找字体文件，并按
模板约定的目标文件名复制，方便同学直接执行 `make import-fonts`。
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROPRIETARY_DIR = PROJECT_ROOT / "fonts" / "proprietary"


CORE_FONT_TARGETS = [
    {
        "dest": "TimesNewRoman-Regular.ttf",
        "label": "Times New Roman Regular",
        "candidates": ["TimesNewRoman-Regular.ttf", "Times New Roman.ttf", "times.ttf"],
    },
    {
        "dest": "TimesNewRoman-Bold.ttf",
        "label": "Times New Roman Bold",
        "candidates": ["TimesNewRoman-Bold.ttf", "Times New Roman Bold.ttf", "timesbd.ttf"],
    },
    {
        "dest": "TimesNewRoman-Italic.ttf",
        "label": "Times New Roman Italic",
        "candidates": ["TimesNewRoman-Italic.ttf", "Times New Roman Italic.ttf", "timesi.ttf"],
    },
    {
        "dest": "TimesNewRoman-BoldItalic.ttf",
        "label": "Times New Roman Bold Italic",
        "candidates": ["TimesNewRoman-BoldItalic.ttf", "Times New Roman Bold Italic.ttf", "timesbi.ttf"],
    },
    {
        "dest": "Arial-Regular.ttf",
        "label": "Arial Regular",
        "candidates": ["Arial-Regular.ttf", "Arial.ttf", "arial.ttf"],
    },
    {
        "dest": "Arial-Bold.ttf",
        "label": "Arial Bold",
        "candidates": ["Arial-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"],
    },
    {
        "dest": "CourierNew-Regular.ttf",
        "label": "Courier New Regular",
        "candidates": ["CourierNew-Regular.ttf", "Courier New.ttf", "cour.ttf"],
    },
    {
        "dest": "CourierNew-Bold.ttf",
        "label": "Courier New Bold",
        "candidates": ["CourierNew-Bold.ttf", "Courier New Bold.ttf", "courbd.ttf"],
    },
    {
        "dest": "SimSun.ttc",
        "label": "宋体",
        "candidates": ["SimSun.ttc", "SimSun.ttf", "宋体.ttc", "宋体.ttf", "simsun.ttc", "simsun.ttf"],
    },
    {
        "dest": "SimHei.ttf",
        "label": "黑体",
        "candidates": ["SimHei.ttf", "黑体.ttf", "simhei.ttf"],
    },
    {
        "dest": "KaiTi.ttf",
        "label": "楷体 / 楷体_GB2312",
        "candidates": ["KaiTi.ttf", "KaiTi_GB2312.ttf", "楷体.ttf", "楷体_GB2312.ttf", "simkai.ttf"],
    },
    {
        "dest": "FangSong_GB2312.ttf",
        "label": "仿宋 / 仿宋_GB2312",
        "candidates": ["FangSong_GB2312.ttf", "FangSong.ttf", "仿宋_GB2312.ttf", "仿宋.ttf", "simfang.ttf"],
    },
    {
        "dest": "FangZhengXiaoBiaoSongJianTi.ttf",
        "label": "方正小标宋简体",
        "candidates": [
            "FangZhengXiaoBiaoSongJianTi.ttf",
            "方正小标宋简体.ttf",
            "方正小标宋简.ttf",
            "FZXBSJW.TTF",
            "FZXBSJW.ttf",
            "FZXBSJW--GB1-0.ttf",
        ],
    },
    {
        "dest": "STXingkai.ttf",
        "label": "华文行楷",
        "candidates": ["STXingkai.ttf", "STXINGKA.TTF", "华文行楷.ttf"],
    },
]

OPTIONAL_FONT_TARGETS = [
    {
        "dest": "STLiti.ttf",
        "label": "华文隶书",
        "candidates": ["STLiti.ttf", "STLITI.TTF", "华文隶书.ttf"],
    }
]


def unique_existing_dirs(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in paths:
        expanded = path.expanduser()
        key = str(expanded)
        if key in seen:
            continue
        seen.add(key)
        if expanded.exists():
            ordered.append(expanded)
    return ordered


def default_search_dirs() -> list[Path]:
    home = Path.home()
    system = platform.system()
    paths: list[Path] = [
        home / "Desktop" / "毕业论文字体",
        home / "Desktop" / "fonts",
        home / "Desktop" / "Fonts",
        home / "Desktop",
    ]

    if system == "Darwin":
        paths.extend(
            [
                Path("/System/Library/Fonts"),
                Path("/System/Library/Fonts/Supplemental"),
                Path("/Library/Fonts"),
                home / "Library" / "Fonts",
                Path("/Applications/wpsoffice.app/Contents/Resources/office6/fonts"),
                Path("/Applications/WPS Office.app/Contents/Resources/office6/fonts"),
            ]
        )
    elif system == "Windows":
        for env_name in ("WINDIR", "SystemRoot"):
            value = os.environ.get(env_name)
            if value:
                paths.append(Path(value) / "Fonts")
        for env_name in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            value = os.environ.get(env_name)
            if not value:
                continue
            base = Path(value)
            paths.extend(
                [
                    base / "WPS Office" / "office6" / "fonts",
                    base / "Kingsoft" / "WPS Office" / "office6" / "fonts",
                ]
            )
        paths.extend(
            [
                Path("C:/Windows/Fonts"),
                Path("C:/WINDOWS/Fonts"),
                Path("C:/Program Files/WPS Office/office6/fonts"),
                Path("C:/Program Files (x86)/WPS Office/office6/fonts"),
                Path("C:/Program Files/Kingsoft/WPS Office/office6/fonts"),
                Path("C:/Program Files (x86)/Kingsoft/WPS Office/office6/fonts"),
            ]
        )
    else:
        paths.extend(
            [
                Path("/usr/share/fonts"),
                Path("/usr/local/share/fonts"),
                home / ".local" / "share" / "fonts",
                Path("/opt/kingsoft/wps-office/office6/fonts"),
                Path("/usr/share/fonts/wps-office"),
            ]
        )

    return unique_existing_dirs(paths)


def index_font_files(search_dirs: list[Path]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        try:
            for path in search_dir.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in {".ttf", ".ttc", ".otf"}:
                    continue
                index.setdefault(path.name.lower(), path)
        except PermissionError:
            continue
    return index


def find_source(font_index: dict[str, Path], candidates: list[str]) -> Path | None:
    for candidate in candidates:
        match = font_index.get(candidate.lower())
        if match is not None:
            return match
    return None


def copy_target(
    target: dict[str, object],
    font_index: dict[str, Path],
    target_dir: Path,
    *,
    force: bool,
    dry_run: bool,
) -> tuple[str, str]:
    dest = target_dir / str(target["dest"])
    if dest.exists() and not force:
        return "skipped", f"{target['label']}: 已存在 {dest.name}"

    source = find_source(font_index, list(target["candidates"]))
    if source is None:
        return "missing", f"{target['label']}: 未找到候选文件"

    if dry_run:
        return "planned", f"{target['label']}: {source} -> {dest.name}"

    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    return "copied", f"{target['label']}: {source} -> {dest.name}"


def import_fonts(
    search_dirs: list[Path],
    target_dir: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
    include_optional: bool = True,
) -> dict[str, list[str]]:
    targets = list(CORE_FONT_TARGETS)
    if include_optional:
        targets.extend(OPTIONAL_FONT_TARGETS)

    font_index = index_font_files(search_dirs)
    result = {"copied": [], "skipped": [], "missing": [], "planned": []}
    for target in targets:
        status, message = copy_target(target, font_index, target_dir, force=force, dry_run=dry_run)
        result[status].append(message)
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="一键导入本机或系统字体到 fonts/proprietary/")
    parser.add_argument("--search-dir", action="append", default=[], help="额外搜索目录，可多次传入")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的目标字体文件")
    parser.add_argument("--dry-run", action="store_true", help="只打印导入计划，不执行复制")
    parser.add_argument("--skip-optional", action="store_true", help="跳过华文隶书等可选字体")
    return parser.parse_args(argv)


def print_result(search_dirs: list[Path], result: dict[str, list[str]], *, dry_run: bool) -> None:
    print("==> 字体导入搜索目录:")
    for path in search_dirs:
        print(f"  - {path}")

    print("\n==> 导入结果")
    for label, title in (
        ("copied", "已复制"),
        ("planned", "导入计划"),
        ("skipped", "已跳过"),
        ("missing", "未找到"),
    ):
        if not result[label]:
            continue
        print(f"  {title}:")
        for item in result[label]:
            print(f"   - {item}")

    print(f"\n目标目录: {PROPRIETARY_DIR}")
    if not dry_run:
        print("\n下一步:")
        print("  1. 运行 python3 scripts/check_fonts.py")
        print("  2. 运行 make")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    extra_dirs = [Path(path).expanduser() for path in args.search_dir]
    search_dirs = unique_existing_dirs(extra_dirs + default_search_dirs())

    if not search_dirs:
        print("未发现可用字体目录。")
        return 1

    print(f"系统: {platform.system()} {platform.release()}")
    result = import_fonts(
        search_dirs,
        PROPRIETARY_DIR,
        force=args.force,
        dry_run=args.dry_run,
        include_optional=not args.skip_optional,
    )
    print_result(search_dirs, result, dry_run=args.dry_run)

    if args.dry_run:
        print(f"\n计划复制: {len(result['planned'])}")
    else:
        print(f"\n已复制: {len(result['copied'])}")
    print(f"已跳过: {len(result['skipped'])}")
    print(f"未找到: {len(result['missing'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
