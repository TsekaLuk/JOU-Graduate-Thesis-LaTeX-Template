# 江苏海洋大学研究生毕业论文 LaTeX 模板

本项目的目标不是“复刻一篇样张论文”，而是提供一个可以正常写作、符合学术规范、并尽量贴近学校参考件的研究生毕业论文模板。

模板设计思路参考了主流高校模板的共同做法，例如 [ThuThesis](https://github.com/tuna/thuthesis)、[SJTUThesis](https://github.com/sjtug/SJTUThesis)、[ustcthesis](https://github.com/ustctug/ustcthesis) 和 [fduthesis](https://github.com/stone-zeng/fduthesis)：

- 用户只改内容入口，不改版式代码
- 特殊页锁版，正文和目录链路保持正常 LaTeX 写作方式
- 图表、目录、参考文献、交叉引用自动生成
- 编译入口尽量简单，默认使用 `latexmk + XeLaTeX`
- 保留像素级回归测试，避免模板迭代时版式退步

## 3 分钟上手

1. 修改 [contents/shared/metadata.tex](contents/shared/metadata.tex) 中的题名、作者、导师、学位信息。
2. 修改 [contents/user/frontmatter-content.tex](contents/user/frontmatter-content.tex) 中的致谢、摘要、关键词、变量表。
3. 修改 [contents/user/body-content.tex](contents/user/body-content.tex) 中的正文示例、表格和插图标题。
4. 修改 [contents/user/backmatter-content.tex](contents/user/backmatter-content.tex) 中的附录、作者简历、原创性声明正文和数据集说明。
5. 运行 `latexmk -xelatex main.tex` 编译论文。

如果你只想先看模板效果，直接编译 [main.tex](main.tex) 即可。
如果你本机已有常用学术字体，可先运行 `make import-fonts` 自动导入到 `fonts/proprietary/`。

## 推荐编辑边界

日常写论文时，优先编辑这些文件：

- [contents/shared/metadata.tex](contents/shared/metadata.tex)
- [contents/user/frontmatter-content.tex](contents/user/frontmatter-content.tex)
- [contents/user/body-content.tex](contents/user/body-content.tex)
- [contents/user/backmatter-content.tex](contents/user/backmatter-content.tex)

[contents/shared/metadata.tex](contents/shared/metadata.tex) 现在也负责这些结构化字段：

- 学位类别、学位级别
- 学位授予单位、培养单位、单位代码
- 培养单位地址、邮编
- 论文语种、学位授予年

通常不要直接修改这些文件，除非你在调整模板样式：

- [styles/jougraduate.cls](styles/jougraduate.cls)
- [styles/jougraduateheadings.sty](styles/jougraduateheadings.sty)
- [contents/frontmatter/](contents/frontmatter)
- [contents/backmatter/](contents/backmatter)

## 当前模板策略

- 封面、授权声明、内封、审阅认定书等学校固定页采用锁版策略。
- 摘要、目录、图表清单、变量表、正文、参考文献采用正常模板链路。
- 研究生模板默认不生成硕士论文不需要的 `Extended Abstract`。
- 通过 `pytest` 保持与参考 Word/PDF 的结构和关键页面位置对齐。

## 与本科生模板的关系

本仓库是同级本科模板工程标准的研究生版本，继续复用：

- 本科生模板直达：[江苏海洋大学本科生毕业论文模板](https://github.com/TsekaLuk/JOU-Undergraduate-Thesis-LaTeX-Template)

- 字体检测与加载系统
- 开源兜底字体
- 跨平台字体兼容测试
- 参考文档 XML 拆解与 PDF 对齐基线

## 验证命令

- `make import-fonts`
- `latexmk -xelatex main.tex`
- `pytest -q`

## QA

### 为什么仓库不直接附带商业字体，以及怎么一键导入。

商业字体大多属于系统字体、Office 字体或商业字库，公共仓库不适合直接再分发。

模板已经提供了两层方案：

- 本地正式字体：把你合法拥有的字体放进 `fonts/proprietary/`
- 一键导入：直接运行 `make import-fonts`，脚本会从 Windows 字体目录、macOS 字体目录、WPS 安装目录和桌面字体目录自动复制并规范命名

如果机器上没有这些正式字体，模板仍然会回退到仓库内置的开源字体，保证能编译、能预览、能继续写论文。

## 开源许可

项目代码采用 [LaTeX Project Public License v1.3c](https://www.latex-project.org/lppl.txt)。
仓库内的开源兜底字体随各自许可证分发；用户本地放入 `fonts/proprietary/` 的专有字体不随仓库再分发，仍受原字体许可约束。
