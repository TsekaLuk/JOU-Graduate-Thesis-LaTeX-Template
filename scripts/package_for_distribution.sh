#!/bin/bash
# 打包研究生论文模板：Overleaf 社区包、Overleaf 完整包和 CTAN 风格发布包

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(grep "ProvidesClass{jougraduate}" "$PROJECT_ROOT/styles/jougraduate.cls" | sed -n 's/.*\[\([0-9]\{4\}\/[0-9]\{2\}\/[0-9]\{2\}\).*/\1/p' | tr '/' '-')"
DIST_DIR="$PROJECT_ROOT/dist"
TEMP_DIR="$PROJECT_ROOT/tmp/packaging"
REPO_URL="$(git -C "$PROJECT_ROOT" remote get-url origin 2>/dev/null || echo "https://github.com/TsekaLuk/JOU-Graduate-Thesis-LaTeX-Template.git")"
MAINTAINER_NAME="${CTAN_MAINTAINER_NAME:-$(git -C "$PROJECT_ROOT" config user.name 2>/dev/null || echo '[Your Name]')}"
MAINTAINER_EMAIL="${CTAN_MAINTAINER_EMAIL:-$(git -C "$PROJECT_ROOT" config user.email 2>/dev/null || echo 'your.email@example.com')}"

echo "=========================================="
echo "JOU 研究生论文模板打包脚本"
echo "版本: $VERSION"
echo "=========================================="

rm -rf "$DIST_DIR" "$TEMP_DIR"
mkdir -p "$DIST_DIR" "$TEMP_DIR"

create_latexmkrc() {
  local target_dir="$1"
  cat > "$target_dir/latexmkrc" <<'EOF'
$pdf_mode = 5;
$postscript_mode = $dvi_mode = 0;
$xelatex = 'xelatex -interaction=nonstopmode -file-line-error %O %S';
$clean_ext = 'aux bbl blg fdb_latexmk fls log out synctex.gz toc toe lof lot';
EOF
  cp "$target_dir/latexmkrc" "$target_dir/.latexmkrc"
}

copy_tree_without_build_files() {
  local source_dir="$1"
  local target_dir="$2"
  cp -r "$source_dir" "$target_dir"
  find "$target_dir" -type f \( -name '*.aux' -o -name '*.log' -o -name '*.bbl' -o -name '*.blg' -o -name '*.xdv' -o -name '*.fdb_latexmk' -o -name '*.fls' \) -delete
}

copy_common_project_files() {
  local target_dir="$1"
  mkdir -p "$target_dir"
  cp "$PROJECT_ROOT/main.tex" "$target_dir/"
  cp "$PROJECT_ROOT/LICENSE" "$target_dir/"
  cp "$PROJECT_ROOT/README.md" "$target_dir/"
  cp -r "$PROJECT_ROOT/figures" "$target_dir/"
  copy_tree_without_build_files "$PROJECT_ROOT/styles" "$target_dir"
  copy_tree_without_build_files "$PROJECT_ROOT/contents" "$target_dir"
  mkdir -p "$target_dir/references"
  cp "$PROJECT_ROOT/references/refs.bib" "$target_dir/references/"
  if [ -f "$PROJECT_ROOT/docs/guides/usage.md" ]; then
    cp "$PROJECT_ROOT/docs/guides/usage.md" "$target_dir/USAGE.md"
  fi
  if [ -d "$PROJECT_ROOT/samples" ]; then
    copy_tree_without_build_files "$PROJECT_ROOT/samples" "$target_dir"
  fi
  create_latexmkrc "$target_dir"
}

echo ""
echo "==> 准备 Overleaf Gallery 轻量社区包..."

OVERLEAF_GALLERY_DIR="$TEMP_DIR/jougraduate-overleaf-gallery"
copy_common_project_files "$OVERLEAF_GALLERY_DIR"
mkdir -p "$OVERLEAF_GALLERY_DIR/fonts"
cp -r "$PROJECT_ROOT/fonts/opensource" "$OVERLEAF_GALLERY_DIR/fonts/"
mkdir -p "$OVERLEAF_GALLERY_DIR/fonts/proprietary"
cat > "$OVERLEAF_GALLERY_DIR/fonts/README.md" <<EOF
# Overleaf Gallery Community Package

This package is intentionally lightweight for Overleaf Gallery distribution.

- Canonical maintained version: ${REPO_URL}
- Open-source fallback fonts are included.
- Local commercial fonts are intentionally omitted.
- For full assets, local packaging, issue tracking and tests, use the GitHub repository.
EOF
echo "# Place legally obtained local fonts here in a full local clone." > "$OVERLEAF_GALLERY_DIR/fonts/proprietary/README.md"

cat > "$OVERLEAF_GALLERY_DIR/OVERLEAF_GALLERY.md" <<EOF
# Overleaf Gallery Release

This is the lightweight community edition for Overleaf Gallery.

- Best for: quick preview and onboarding
- Canonical maintained version: ${REPO_URL}
- Full assets, packaging scripts, CI, and issue tracking live on GitHub
EOF

(
  cd "$TEMP_DIR"
  zip -qr "$DIST_DIR/jougraduate-overleaf-gallery-${VERSION}.zip" jougraduate-overleaf-gallery -x "*.DS_Store" "*.git*"
)
echo "✓ Overleaf Gallery 包已生成: $DIST_DIR/jougraduate-overleaf-gallery-${VERSION}.zip"

echo ""
echo "==> 准备 Overleaf 完整上传包..."

OVERLEAF_DIR="$TEMP_DIR/jougraduate-overleaf"
copy_common_project_files "$OVERLEAF_DIR"
cp -r "$PROJECT_ROOT/fonts" "$OVERLEAF_DIR/"
rm -rf "$OVERLEAF_DIR/fonts/proprietary"
mkdir -p "$OVERLEAF_DIR/fonts/proprietary"
echo "# 请在本地把合法商业字体放入此目录；Overleaf 环境默认使用 fonts/opensource/ 中的字体。" > "$OVERLEAF_DIR/fonts/proprietary/README.md"

(
  cd "$TEMP_DIR"
  zip -qr "$DIST_DIR/jougraduate-overleaf-${VERSION}.zip" jougraduate-overleaf -x "*.DS_Store" "*.git*"
)
echo "✓ Overleaf 完整包已生成: $DIST_DIR/jougraduate-overleaf-${VERSION}.zip"

echo ""
echo "==> 准备 CTAN 风格发布包..."

CTAN_DIR="$TEMP_DIR/jougraduate"
mkdir -p "$CTAN_DIR"/{tex,doc,source}
cp "$PROJECT_ROOT"/styles/*.cls "$CTAN_DIR/tex/"
cp "$PROJECT_ROOT"/styles/*.sty "$CTAN_DIR/tex/"

mkdir -p "$CTAN_DIR/doc/examples/contents"
mkdir -p "$CTAN_DIR/doc/examples/references"
mkdir -p "$CTAN_DIR/doc/examples/samples"
mkdir -p "$CTAN_DIR/doc/figures"

cp "$PROJECT_ROOT/README.md" "$CTAN_DIR/doc/"
cp "$PROJECT_ROOT/LICENSE" "$CTAN_DIR/doc/"
if [ -f "$PROJECT_ROOT/docs/guides/usage.md" ]; then
  cp "$PROJECT_ROOT/docs/guides/usage.md" "$CTAN_DIR/doc/USAGE.md"
fi
cp "$PROJECT_ROOT/main.tex" "$CTAN_DIR/doc/examples/"
copy_tree_without_build_files "$PROJECT_ROOT/contents" "$CTAN_DIR/doc/examples"
cp "$PROJECT_ROOT/references/refs.bib" "$CTAN_DIR/doc/examples/references/"
cp "$PROJECT_ROOT/figures/"* "$CTAN_DIR/doc/figures/"
if [ -d "$PROJECT_ROOT/samples" ]; then
  copy_tree_without_build_files "$PROJECT_ROOT/samples" "$CTAN_DIR/doc/examples"
fi

cat > "$CTAN_DIR/README" <<EOF
JOU Graduate Thesis LaTeX Template
==================================

Version: $VERSION
License: LPPL 1.3c

This package provides a LaTeX thesis template for graduate students at Jiangsu Ocean University (JOU).

Features:
- Cross-platform font support (Linux, macOS, Windows)
- Pixel-aware alignment checks against the graduate reference PDF
- Locked special pages with normal LaTeX body-writing workflow
- GitHub-maintained canonical distribution

Installation:
1. Copy files from tex/ to your local TEXMF tree
2. Run 'texhash' to update the filename database

Documentation:
- README.md: onboarding and project overview
- USAGE.md: writing guide

For more information, visit:
${REPO_URL}

Maintainer: ${MAINTAINER_NAME} <${MAINTAINER_EMAIL}>
EOF

(
  cd "$TEMP_DIR"
  zip -qr "$DIST_DIR/jougraduate-ctan-${VERSION}.zip" jougraduate -x "*.DS_Store" "*.git*"
)
echo "✓ CTAN 风格包已生成: $DIST_DIR/jougraduate-ctan-${VERSION}.zip"

echo ""
echo "==> 生成环境一致性检查配置..."

cat > "$DIST_DIR/environment-check.yml" <<'EOF'
name: JOU Graduate Thesis Environment Check

texlive:
  minimum_version: "2020"
  required_packages:
    - xetex
    - ctex
    - fontspec
    - geometry
    - fancyhdr
    - titletoc
    - graphicx
    - amsmath
    - natbib
    - hyperref
    - cleveref
    - caption
    - booktabs
    - tabularx
    - multirow
    - longtable
    - listings
    - xcolor
    - tikz
    - pgfplots

fonts:
  required:
    - "Times New Roman (or Tinos fallback)"
    - "SimSun/STSong (or Noto Serif CJK fallback)"
    - "SimHei/STHeiti (or Noto Sans CJK fallback)"
    - "KaiTi/STKaiti (or LXGW WenKai fallback)"

tools:
  required:
    - xelatex
    - bibtex
  optional:
    - latexmk
    - pdfinfo
    - pdftoppm
    - pdftotext

validation:
  checks:
    - "PDF generated successfully"
    - "Fonts embedded"
    - "Cross-references resolved"
    - "Bibliography compiled"
EOF
echo "✓ 环境检查配置已生成: $DIST_DIR/environment-check.yml"

cat > "$DIST_DIR/UPLOAD-CHECKLIST.md" <<EOF
# 上传清单

## Overleaf 上传步骤

### 社区版
1. 登录 Overleaf
2. 上传 \`jougraduate-overleaf-gallery-${VERSION}.zip\`
3. 选择 XeLaTeX 作为编译器
4. 验证首页、摘要、目录和正文页正常生成

### 完整版
1. 登录 Overleaf
2. 上传 \`jougraduate-overleaf-${VERSION}.zip\`
3. 如需正式字体，请在本地仓库导入后再重新打包

## GitHub 发布建议

- 轻量预览包：\`jougraduate-overleaf-gallery-${VERSION}.zip\`
- 完整上传包：\`jougraduate-overleaf-${VERSION}.zip\`
- CTAN 风格包：\`jougraduate-ctan-${VERSION}.zip\`

Canonical repository:
${REPO_URL}
EOF
echo "✓ 上传清单已生成: $DIST_DIR/UPLOAD-CHECKLIST.md"

echo ""
echo "=========================================="
echo "打包完成"
echo "=========================================="
echo "产物目录: $DIST_DIR"
