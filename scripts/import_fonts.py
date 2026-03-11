#!/usr/bin/env python3
"""
一键导入本地字体到 fonts/proprietary/。

目标：
1. 从常见系统目录、WPS 目录和桌面字体目录中自动查找字体
2. 复制到仓库 fonts/proprietary/ 并规范命名
3. 让同学在本地只需执行一次 make import-fonts
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

HOME = Path.home()

WINDOWS_FONT_DIRS = [
    Path("C:/Windows/Fonts"),
    Path("C:/WINDOWS/Fonts"),
]

for env_name in ("WINDIR", "SystemRoot"):
    value = os.environ.get(env_name)
    if value:
        WINDOWS_FONT_DIRS.insert(0, Path(value) / "Fonts")

WPS_FONT_DIRS = [
    Path("/Applications/wpsoffice.app/Contents/Resources/office6/fonts"),
    Path("/Applications/WPS Office.app/Contents/Resources/office6/fonts"),
    Path("/opt/kingsoft/wps-office/office6/fonts"),
    Path("/usr/share/fonts/wps-office"),
    Path("C:/Program Files/WPS Office/office6/fonts"),
    Path("C:/Program Files (x86)/WPS Office/office6/fonts"),
    Path("C:/Program Files/Kingsoft/WPS Office/office6/fonts"),
    Path("C:/Program Files (x86)/Kingsoft/WPS Office/office6/fonts"),
]

for env_name in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
    value = os.environ.get(env_name)
    if value:
        base = Path(value)
        WPS_FONT_DIRS.extend(
            [
                base / "WPS Office" / "office6" / "fonts",
                base / "Kingsoft" / "WPS Office" / "office6" / "fonts",
            ]
        )

MAC_FONT_DIRS = [
    Path("/System/Library/Fonts"),
    Path("/Library/Fonts"),
    HOME / "Library" / "Fonts",
]

DESKTOP_FONT_DIRS = [
    HOME / "Desktop" / "毕业论文字体",
    HOME / "Desktop" / "fonts",
    HOME / "Desktop" / "Fonts",
    HOME / "Desktop",
]

FONT_IMPORT_MAP = {
    "TimesNewRoman-Regular.ttf": [
        "TimesNewRoman-Regular.ttf",
        "times.ttf",
    ],
    "TimesNewRoman-Bold.ttf": [
        "TimesNewRoman-Bold.ttf",
        "timesbd.ttf",
    ],
    "TimesNewRoman-Italic.ttf": [
        "TimesNewRoman-Italic.ttf",
        "timesi.ttf",
    ],
    "TimesNewRoman-BoldItalic.ttf": [
        "TimesNewRoman-BoldItalic.ttf",
        "timesbi.ttf",
    ],
    "Arial-Regular.ttf": [
        "Arial-Regular.ttf",
        "arial.ttf",
    ],
    "Arial-Bold.ttf": [
        "Arial-Bold.ttf",
        "arialbd.ttf",
    ],
    "CourierNew-Regular.ttf": [
        "CourierNew-Regular.ttf",
        "cour.ttf",
    ],
    "CourierNew-Bold.ttf": [
        "CourierNew-Bold.ttf",
        "courbd.ttf",
    ],
    "SimSun.ttc": [
        "SimSun.ttc",
        "SimSun.ttf",
        "宋体.ttc",
        "宋体.ttf",
        "simsun.ttc",
        "simsun.ttf",
    ],
    "SimHei.ttf": [
        "SimHei.ttf",
        "黑体.ttf",
        "simhei.ttf",
    ],
    "KaiTi.ttf": [
        "KaiTi.ttf",
        "KaiTi_GB2312.ttf",
        "楷体.ttf",
        "simkai.ttf",
    ],
    "FangSong_GB2312.ttf": [
        "FangSong_GB2312.ttf",
        "FangSong.ttf",
        "仿宋_GB2312.ttf",
        "simfang.ttf",
    ],
    "FangZhengXiaoBiaoSongJianTi.ttf": [
        "FangZhengXiaoBiaoSongJianTi.ttf",
        "方正小标宋简.ttf",
        "FZXBSJW.TTF",
        "FZXBSJW.ttf",
    ],
    "STXingkai.ttf": [
        "STXingkai.ttf",
        "STXINGKA.TTF",
        "华文行楷.ttf",
    ],
    "STLiti.ttf": [
        "STLiti.ttf",
        "STLITI.TTF",
        "华文隶书.ttf",
    ],
}


def build_search_dirs() -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []
    for path in DESKTOP_FONT_DIRS + WINDOWS_FONT_DIRS + MAC_FONT_DIRS + WPS_FONT_DIRS:
        if path.exists() and path not in seen:
            ordered.append(path)
            seen.add(path)
    return ordered


def index_font_files(search_dirs: list[Path]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for root in search_dirs:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".ttf", ".ttc", ".otf"}:
                continue
            key = path.name.lower()
            index.setdefault(key, path)
    return index


def import_fonts(search_dirs: list[Path], target_dir: Path, force: bool = False) -> dict[str, list[str]]:
    target_dir.mkdir(parents=True, exist_ok=True)
    font_index = index_font_files(search_dirs)
    result = {"copied": [], "existing": [], "missing": []}

    for target_name, candidates in FONT_IMPORT_MAP.items():
        target_path = target_dir / target_name
        if target_path.exists() and not force:
            result["existing"].append(target_name)
            continue

        source_path = None
        for candidate in candidates:
            source_path = font_index.get(candidate.lower())
            if source_path is not None:
                break

        if source_path is None:
            result["missing"].append(target_name)
            continue

        shutil.copyfile(source_path, target_path)
        result["copied"].append(f"{target_name} <- {source_path}")

    return result


def print_result(search_dirs: list[Path], result: dict[str, list[str]]) -> None:
    print("==> 字体导入搜索目录")
    for path in search_dirs:
        print(f"   - {path}")

    print("\n==> 导入结果")
    if result["copied"]:
        print("  已复制:")
        for item in result["copied"]:
            print(f"   - {item}")

    if result["existing"]:
        print("  已存在:")
        for item in result["existing"]:
            print(f"   - {item}")

    if result["missing"]:
        print("  未找到:")
        for item in result["missing"]:
            print(f"   - {item}")

    print(f"\n目标目录: {PROPRIETARY_DIR}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import common thesis fonts into fonts/proprietary")
    parser.add_argument("--force", action="store_true", help="overwrite existing target files")
    args = parser.parse_args()

    search_dirs = build_search_dirs()
    if not search_dirs:
        print("未发现可用字体目录。")
        return 1

    print(f"系统: {platform.system()} {platform.release()}")
    result = import_fonts(search_dirs, PROPRIETARY_DIR, force=args.force)
    print_result(search_dirs, result)

    if result["copied"]:
        print("\n==> 已完成字体导入")
    elif not result["missing"]:
        print("\n==> 目标字体已齐全，无需重复导入")
    else:
        print("\n==> 未导入到任何新字体，请把字体放到常见目录后重试")

    return 0


if __name__ == "__main__":
    sys.exit(main())
