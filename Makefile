MAIN = main
TEX = xelatex
BIB = bibtex
TEXFLAGS = -interaction=nonstopmode -halt-on-error
THESIS_DEPS = $(MAIN).tex \
	$(wildcard styles/*.sty) \
	$(wildcard styles/*.cls) \
	$(wildcard contents/shared/*.tex) \
	$(wildcard contents/frontmatter/*.tex) \
	$(wildcard contents/chapters/*.tex) \
	$(wildcard contents/backmatter/*.tex) \
	$(wildcard contents/appendices/*.tex) \
	$(wildcard references/*.bib)

.PHONY: all fonts import-fonts clean cleanall view help test

all: fonts $(MAIN).pdf

fonts:
	@echo "==> 检查仓库字体资源..."
	python3 scripts/download_fonts.py

import-fonts:
	@echo "==> 从常见位置导入本地字体..."
	python3 scripts/import_fonts.py

$(MAIN).pdf: $(THESIS_DEPS)
	@echo "==> 第1次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 处理参考文献..."
	$(BIB) $(MAIN)
	@echo "==> 第2次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 第3次编译..."
	$(TEX) $(TEXFLAGS) $(MAIN)
	@echo "==> 编译完成: $(MAIN).pdf"

clean:
	@echo "==> 清理临时文件..."
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.loa *.lol
	rm -f *.fls *.fdb_latexmk *.synctex.gz *.xdv *.nav *.snm *.vrb
	rm -f *.nlo *.nls *.ilg *.ind *.idx
	rm -f contents/frontmatter/*.aux contents/chapters/*.aux contents/backmatter/*.aux contents/appendices/*.aux

cleanall: clean
	@echo "==> 删除主 PDF..."
	rm -f $(MAIN).pdf

view: $(MAIN).pdf
	@echo "==> 打开 PDF..."
	@if [ "$(shell uname)" = "Darwin" ]; then \
		open $(MAIN).pdf; \
	elif [ "$(shell uname)" = "Linux" ]; then \
		xdg-open $(MAIN).pdf; \
	else \
		echo "请手动打开 $(MAIN).pdf"; \
	fi

test: $(MAIN).pdf
	pytest -q

help:
	@echo "江苏海洋大学研究生毕业论文 LaTeX 模板"
	@echo ""
	@echo "可用命令:"
	@echo "  make        - 下载字体并编译主模板"
	@echo "  make import-fonts - 从系统/WPS/桌面字体目录导入常用字体到 fonts/proprietary"
	@echo "  make test   - 编译主模板并运行 pytest 合同"
	@echo "  make clean  - 清理临时文件"
	@echo "  make cleanall - 连同 main.pdf 一起清理"
	@echo "  make view   - 打开 main.pdf"
