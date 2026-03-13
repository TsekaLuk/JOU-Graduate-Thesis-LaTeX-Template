# 研究生模板 UX 打磨设计

日期：2026-03-13

## 目标

把模板进一步收成“写作者优先”的使用体验：

- 第一次打开仓库时，能快速知道先改哪里、先跑什么命令
- 日常写作时，不需要反复理解模板内部结构
- 常见问题优先在入口层解决，而不是让用户直接改类文件

## 现状问题

- README 信息完整，但首次上手路径仍然偏长
- `contents/setup.tex` 高低频字段混在一起，新手不容易判断先改哪些
- Makefile 缺少面向首次使用者的组合入口
- `docs/guides/usage.md` 更像补充说明，不够任务导向

## 方案

采用“Writer-first UX 层”：

1. README 顶部增加首次使用与常见任务入口
2. `contents/setup.tex` 明确拆成“必改字段 / 常用页面开关 / 低频补充字段”
3. Makefile 增加 `doctor` 与 `quickstart`
4. 使用指南改成任务导向，减少与 README 的重复解释
5. 用测试把这些入口固化，避免后续回退

## 约束

- 不改变主模板排版逻辑
- 不引入新的配置格式，继续沿用当前 `\JOUSetup`
- 不重命名已有用户入口文件，避免破坏兼容性

## 验证

- `pytest -q tests/test_repository_workflow.py tests/test_format_compliance.py`
- 目视检查 README、usage guide、`contents/setup.tex` 和 `make help`
