MAIN = main
BODY_SAMPLE_TEX = samples/body-sample.tex
BODY_SAMPLE_PDF = body-sample.pdf
TEX = xelatex
BIB = bibtex
TEXFLAGS = -interaction=nonstopmode -halt-on-error

THESIS_DEPS = $(MAIN).tex \
	$(wildcard .latexmkrc) \
	$(wildcard styles/*.sty) \
	$(wildcard styles/*.cls) \
	$(wildcard contents/*.tex) \
	$(wildcard contents/shared/*.tex) \
	$(wildcard contents/user/*.tex) \
	$(wildcard contents/user/chapters/*.tex) \
	$(wildcard contents/samples/*.tex) \
	$(wildcard contents/frontmatter/*.tex) \
	$(wildcard contents/chapters/*.tex) \
	$(wildcard contents/backmatter/*.tex) \
	$(wildcard contents/appendices/*.tex) \
	$(wildcard references/*.bib)

BODY_SAMPLE_DEPS = $(BODY_SAMPLE_TEX) \
	$(wildcard .latexmkrc) \
	$(wildcard styles/*.sty) \
	$(wildcard styles/*.cls) \
	$(wildcard contents/*.tex) \
	$(wildcard contents/shared/*.tex) \
	$(wildcard contents/user/*.tex) \
	$(wildcard contents/samples/*.tex) \
	$(wildcard contents/chapters/*.tex)

.PHONY: all fonts import-fonts env-check doctor quickstart new-chapter clean cleanall view help test cover-diff readme-images package wordcount

all: fonts $(MAIN).pdf $(BODY_SAMPLE_PDF)

fonts:
	@echo "==> 检查仓库字体资源..."
	python3 scripts/download_fonts.py

import-fonts:
	@echo "==> 导入本机标准字体..."
	python3 scripts/import_fonts.py

env-check:
	@echo "==> 检查本地环境..."
	python3 scripts/check_environment.py

doctor:
	@echo "==> 诊断字体与编译环境..."
	python3 scripts/check_fonts.py
	@$(MAKE) --no-print-directory env-check

quickstart:
	@echo "==> 首次使用快速流程..."
	@$(MAKE) --no-print-directory import-fonts
	@$(MAKE) --no-print-directory doctor
	@$(MAKE) --no-print-directory all

new-chapter:
	@if [ -z "$(NAME)" ] || [ -z "$(TITLE_CN)" ] || [ -z "$(TITLE_EN)" ]; then \
		echo '用法: make new-chapter NAME=08-literature-review TITLE_CN=文献综述 TITLE_EN="Literature Review"'; \
		exit 2; \
	fi
	@echo "==> 创建新章节..."
	python3 scripts/new_chapter.py --name "$(NAME)" --title-cn "$(TITLE_CN)" --title-en "$(TITLE_EN)"

$(MAIN).pdf: $(THESIS_DEPS)
	@echo "==> 第1次编译主模板..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 处理参考文献..."
	-$(BIB) $(MAIN)
	@echo "==> 第2次编译主模板..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 第3次编译主模板..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 编译完成: $(MAIN).pdf"

$(BODY_SAMPLE_PDF): $(BODY_SAMPLE_DEPS)
	@echo "==> 编译正文样页基线..."
	$(TEX) $(TEXFLAGS) $(BODY_SAMPLE_TEX)
	@echo "==> 第2次编译正文样页基线..."
	$(TEX) $(TEXFLAGS) $(BODY_SAMPLE_TEX)
	@echo "==> 正文样页生成完成: $(BODY_SAMPLE_PDF)"

cover-diff: $(MAIN).pdf
	python3 scripts/generate_cover_diff.py

readme-images: $(MAIN).pdf $(BODY_SAMPLE_PDF)
	python3 scripts/generate_readme_images.py

package:
	bash scripts/package_for_distribution.sh

clean:
	@echo "==> 清理临时文件..."
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.toe *.lof *.lot *.loa *.lol
	rm -f *.fls *.fdb_latexmk *.synctex.gz *.xdv *.nav *.snm *.vrb
	rm -f *.nlo *.nls *.ilg *.ind *.idx
	rm -f body-sample.aux body-sample.log body-sample.out body-sample.fls body-sample.fdb_latexmk body-sample.xdv
	rm -f contents/frontmatter/*.aux contents/chapters/*.aux contents/backmatter/*.aux contents/appendices/*.aux

cleanall: clean
	@echo "==> 删除 PDF 文件..."
	rm -f $(MAIN).pdf $(BODY_SAMPLE_PDF)

view: $(MAIN).pdf
	@echo "==> 打开 PDF..."
	@if [ "$(shell uname)" = "Darwin" ]; then \
		open $(MAIN).pdf; \
	elif [ "$(shell uname)" = "Linux" ]; then \
		xdg-open $(MAIN).pdf; \
	else \
		echo "请手动打开 $(MAIN).pdf"; \
	fi

test: $(MAIN).pdf $(BODY_SAMPLE_PDF)
	pytest -q

wordcount:
	@echo "==> 统计正文章节字数..."
	@find contents/user/chapters -name "*.tex" -exec cat {} \; | \
		sed 's/\\[a-zA-Z@]*{//g' | sed 's/}//g' | \
		sed 's/%.*//g' | sed '/^$$/d' | wc -m
	@echo "注：此为粗略估计，实际字数以学校要求工具为准"

help:
	@echo "江苏海洋大学研究生毕业论文 LaTeX 模板"
	@echo ""
	@echo "可用命令:"
	@echo "  make              - 下载字体并编译主模板与正文样页"
	@echo "  make fonts        - 下载/校验仓库内置开源字体"
	@echo "  make import-fonts - 从系统 / 桌面 / WPS 目录导入本机字体"
	@echo "  make env-check    - 检查 XeLaTeX / Poppler / 关键包与仓库资产"
	@echo "  make doctor       - 诊断字体状态并检查本地编译环境"
	@echo "  make quickstart   - 一键执行 import-fonts -> doctor -> make"
	@echo "  make new-chapter  - 新建章节并自动接入正文入口"
	@echo "  make body-sample.pdf - 编译正文样页基线 PDF"
	@echo "  make cover-diff   - 生成封面 overlay/diff/checker 对比图"
	@echo "  make readme-images - 生成 README 用的预览截图"
	@echo "  make package      - 生成 Overleaf / CTAN 风格发布包"
	@echo "  make test         - 编译主模板与正文样页并运行 pytest 合同"
	@echo "  make wordcount    - 粗略统计正文章节字数"
	@echo "  make clean        - 清理临时文件"
	@echo "  make cleanall     - 连同 PDF 一起清理"
	@echo "  make view         - 打开 main.pdf"
