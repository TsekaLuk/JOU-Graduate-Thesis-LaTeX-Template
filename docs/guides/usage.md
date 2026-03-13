# 使用指南

## 第一次打开仓库先做什么

推荐直接运行：

```bash
make quickstart
```

这条命令会顺序执行：

```bash
make import-fonts
make doctor
make
```

如果你只想先查问题，不想立刻编译，运行：

```bash
make doctor
```

## 你真正需要改哪些文件

日常写论文时，只需要改这几处：

- `contents/setup.tex`
- `contents/user/frontmatter-content.tex`
- `contents/user/chapters/*.tex`
- `contents/user/backmatter-content.tex`

模板样式和锁版页通常不用碰：

- `styles/jougraduate.cls`
- `styles/jougraduateheadings.sty`
- `contents/frontmatter/*.tex`
- `contents/backmatter/*.tex`

## 推荐写作流程

1. 先在 `setup.tex` 填题名、作者、导师、学位信息。
2. 在 `frontmatter-content.tex` 填致谢、摘要、关键词、变量表。
3. 在 `contents/user/chapters/` 下按章节写正文，默认 starter 已经给到 `01-07`。
4. 在 `backmatter-content.tex` 填附录、作者简历、原创性声明正文和数据集说明。
5. 运行 `make` 或 `latexmk -xelatex main.tex` 持续预览。

## 新增章节

推荐命令：

```bash
make new-chapter NAME=08-literature-review TITLE_CN=文献综述 TITLE_EN="Literature Review"
```

这会自动生成章节文件并接入 `contents/chapters/mainmatter.tex`。

如果你只想看会生成什么：

```bash
python3 scripts/new_chapter.py --name 08-literature-review --title-cn 文献综述 --title-en "Literature Review" --dry-run
```

这样做比手工复制文件和维护聚合入口更稳，也更接近成熟高校模板的写作方式。

## 常用页面开关

在 `contents/setup.tex` 里可以直接控制这些部分是否输出：

- `blind-review`
- `include-acknowledgements`
- `include-appendix`
- `include-author-resume`
- `include-originality`
- `include-dataset`

推荐理解方式：

- `blind-review = true`：匿名评审版。会自动隐藏作者、导师、学号、培养单位等识别信息，并关闭致谢、作者简历、原创性声明页面。
- 其他 `include-*`：普通模式下的页面显隐开关。

## 推荐命令

```bash
make quickstart
make doctor
make import-fonts
make
make new-chapter NAME=08-literature-review TITLE_CN=文献综述 TITLE_EN="Literature Review"
make wordcount
make test
make cover-diff
make readme-images
```

Windows 用户可以直接运行仓库根目录下的 `build.bat`。

## 常见任务

- 第一次跑通模板：`make quickstart`
- 检查字体和环境：`make doctor`
- 只导入本机正式字体：`make import-fonts`
- 新增章节：`make new-chapter ...`
- 正式编译：`make`
- 跑回归：`make test`
- 生成 README 预览图：`make readme-images`

## 字体建议

- 最优：导入本机合法标准字体，运行 `make import-fonts`
- 次优：使用系统已有的宋体、黑体、楷体、Times New Roman
- 兜底：仓库内置开源字体，适合预览和协作

如果不同机器命中的字体层级不同，通常仍然能编译，但行宽、分页和标题换行可能会有轻微差异。

## Overleaf 使用边界

Overleaf 适合快速预览，不适合最终高保真提交。正式版本仍建议在本地用 XeLaTeX 编译，并优先导入标准学术字体。
