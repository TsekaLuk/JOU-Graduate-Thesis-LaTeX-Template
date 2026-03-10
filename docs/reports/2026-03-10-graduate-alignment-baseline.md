# 研究生论文对齐基线报告

日期：2026-03-10

## 本轮输出

- 建立了研究生论文主模板 `styles/jougraduate.cls`
- 补齐了 `references/.doc -> .docx -> unpacked XML -> WPS PDF` 的参考链路
- 将主模板拆分成封面、声明、摘要、目录、正文、附录、后置页的页面族
- 建立了 `pytest` 合同并接入关键页面的参考对齐检查

## 当前模板状态

- 编译产物：`main.pdf`
- 当前页数：19 页
- 编译方式：XeLaTeX + BibTeX
- 字体模式：`wps-compat`

## 当前测试结果

- `pytest -q`
- 结果：`67 passed`

## 说明

- 参考 PDF 共 22 页，其中包含 `Extended Abstract`。
- 当前模板默认不生成 `Extended Abstract`，因此页面映射为 19 页，这是有意为之的研究生模板收敛策略。
