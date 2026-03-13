# 正文章节目录

这里放的是“你真正会长期编辑的正文文件”。

当前仓库已经带了一个更像真实论文的 starter：

- `01-introduction.tex`
- `02-experiment-research.tex`
- `03-cyclonic-field.tex`
- `04-bubble-particle-interaction.tex`
- `05-process-optimization.tex`
- `06-flotation-kinetics.tex`
- `07-engineering-application.tex`

如果你只是想开始写论文，最简单的做法是直接把这些章节改成自己的内容。

## 推荐新增章节方式

不要手工复制和接线，直接运行：

```bash
make new-chapter NAME=08-literature-review TITLE_CN=文献综述 TITLE_EN="Literature Review"
```

这条命令会自动：

1. 基于 `_template.tex` 生成新章节文件
2. 自动接入 `contents/chapters/mainmatter.tex`
3. 保持正文入口顺序稳定

如果你只想预览将会生成什么内容：

```bash
python3 scripts/new_chapter.py --name 08-literature-review --title-cn 文献综述 --title-en "Literature Review" --dry-run
```
