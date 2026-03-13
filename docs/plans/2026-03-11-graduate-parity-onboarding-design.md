# 研究生模板对标本科模板的质量与 UX 升级设计

日期：2026-03-11

## 目标

在不扩展到本科表单范围的前提下，把研究生毕业论文模板的工程质量、发布链路和用户 onboarding 体验提升到接近本科模板的水平。

本轮只覆盖研究生论文主模板，不引入本科仓库中的配套表单、专项摘要模板或额外业务范围。

## 设计原则

- 复用本科仓库里已经验证过的成熟工程能力，而不是为研究生仓库重新发明一套。
- 特殊页继续保持研究生模板现有的锁版策略，不为追求抽象而牺牲对齐质量。
- 用户入口尽量收敛到 `README.md`、`Makefile`、`contents/shared/metadata.tex` 和 `contents/user/*.tex`。
- 发布脚本、预览资产、测试合同必须和研究生仓库的真实结构一致，不能再保留本科残留。

## 方案选择

### 方案 A：直接迁移本科成熟能力并按研究生范围裁剪

把本科仓库中成熟的打包脚本、README onboarding 结构、Makefile 目标、预览图片生成脚本、环境检查脚本和字体导入 CLI 迁过来，再按研究生模板的页面结构、参考 PDF 和文件布局做裁剪。

优点：

- 风险最低
- 用户体验提升最快
- 可以最大程度共享维护经验

缺点：

- 需要仔细清理本科残留命名和路径

### 方案 B：研究生仓库独立重写一套工程链路

优点：

- 结构更“纯”

缺点：

- 会重复踩本科模板已经解决过的坑
- 发布和测试细节更容易漏

本轮采用方案 A。

## 具体设计

### 1. 发布链路

重写 `scripts/package_for_distribution.sh`，确保：

- 从 `styles/jougraduate.cls` 读取版本
- 包名、文案、仓库链接全部切换为研究生模板
- 只打包研究生模板实际存在的文件
- CTAN/Overleaf 说明文案不再提到本科模板、18 份表单或不存在的英文 README

同时保留本科仓库中已经验证过的 3 类产物：

- Overleaf Gallery 轻量包
- Overleaf 完整上传包
- CTAN 风格发布包

### 2. README onboarding

把当前 README 扩成接近本科模板的 onboarding 文档，但内容只保留研究生论文范围：

- 项目简介
- 发布渠道
- 核心特性
- 预览图
- 模板范围
- 快速开始
- 本地编译与字体导入
- AI 工具辅助写作
- Overleaf 使用边界
- QA
- 开源许可

不引入本科表单清单和不适用于研究生模板的内容。

### 3. 预览资产与命令

补齐本科仓库里成熟的“自检即出图”能力：

- `scripts/generate_cover_diff.py`
- `scripts/generate_readme_images.py`
- `scripts/check_environment.py`

并在 `Makefile` 中增加：

- `body-sample.pdf`
- `cover-diff`
- `readme-images`
- `env-check`
- 更完整的 `help`

研究生仓库的 README 图片将基于研究生参考 PDF 和研究生主模板页生成，不复用本科截图。

### 4. 字体导入与测试

把 `scripts/import_fonts.py` 的 CLI 抬到本科同级：

- `--search-dir`
- `--dry-run`
- `--skip-optional`
- `--force`

同时仍以研究生模板当前所需字体集合为准，不为了追平 CLI 而改变字体策略。

测试层补到同类水平：

- 保留现有研究生对齐合同
- 为字体导入 CLI 增加更细的参数级测试
- 为 packaging/README 关键资产增加仓库合同测试
- 为 README 图片生成与正文样页目标增加存在性和工作流测试

## 成功标准

- `scripts/package_for_distribution.sh` 可以在研究生仓库内完成一次成功打包
- README 能独立承担首次 onboarding
- `make help`、`make import-fonts`、`make cover-diff`、`make readme-images`、`make test` 都有明确用途
- 新增的脚本和测试在当前仓库结构下可运行
- 不引入本科模板范围外的功能
