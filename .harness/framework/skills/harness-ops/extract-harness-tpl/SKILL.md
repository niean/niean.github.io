---
name: extract-harness-tpl
description: 从当前项目提取可复用的 Harness 工程模板
---

# Skill: 提取Harness模板

自动执行约束：在用户指定目标目录下，新建/修改文件无需逐一确认。

## 上下文管理

禁止通过 subagent 读取（易截断），禁止一次性全读。必须分批流水线：按目录分组，每组"读取 -> 蒸馏 -> 写入"后再处理下一组。

## 步骤

### Step 1 -- 确认输出目录
默认目录：./locals/harness_tpl/

### Step 2 -- 分批蒸馏写入
扫描项目根目录的 CLAUDE.md、AGENTS.md 和 .harness/ 下全部目录与文件，按目录自动分组（每个一级子目录为一组，根级文件合为一组），逐组执行"读取 -> 蒸馏 -> 写入"

蒸馏规则：
1. CLAUDE.md：直接拷贝，无需修改内容（兼容Claude Code项目环境）
2. AGENTS.md+FRAMEWORK.md+PROJECT.md+README：剥离项目专属信息，替换为 `{{占位符}}`
3. 保留通用框架/结构/流程
4. 通用规范原文保留；项目规范保留骨架，专属条目替换占位符
5. Subskills 目录仅含通用模板 scan-dimension.md，直接拷贝；扫描维度定义在 `.harness/PROJECT.md` 中，随项目规范一起蒸馏
6. .harness/knowledge/ 和 .harness/prd/ 文件保留结构，正文替换占位符；特例：.harness/prd/03-prd-specs.md也需要蒸馏为模板
7. .harness/plans/、.harness/specs/ 保留目录结构；特例：.harness/plans/debt-tracker.md 也需要蒸馏为模板
8. 禁用 emoji/加粗/斜体
9. 蒸馏判断标准是"内容归属"而非"内容是否具体"：框架自身的版本历史、设计哲学、约束声明等属于框架元数据，应原文保留；仅项目专属信息（项目名、技术栈、业务规则等）才替换为占位符

### Step 3 -- 清理多余文件
比对目标目录，排除 .git/、LICENSE、.DS_Store、node_modules/、*.log 文件；其余不在源目录中的文件经确认后删除。

### Step 4 -- 验证 `[CONFIRM]`

读取同目录下 `references/scan-harness-tpl.md` 获取扫描维度定义，对目标目录执行全维度扫描。

执行方式：
1. 从当前项目 PROJECT.md 提取项目名称和关键业务术语作为维度1搜索关键词
2. 按维度1-5顺序扫描目标目录所有 .md 文件
3. 维度6（版本漂移）：以当前项目 `.harness/framework/` 为基准，比对目标目录同名文件
4. 按 references/scan-harness-tpl.md 报告格式输出扫描结果

问题数为0时直接进入下一个Step；否则结束当前回复，等待用户确认修复范围，修复后对目标目录全量重扫全部维度（最多循环 3 轮）；如仍有问题，将残留问题列入报告标记为'待人工处理'后进入下一个Step。

修复约束：
- AI-READONLY 文件（agents/、prd/、guides/）：输出修改建议，逐个经用户确认后执行
- 其他文件：直接修复
- 修复后回归维度5（引用有效性）检查

### Step 5 -- 输出报告
文件清单、验证结果、占位符汇总。
