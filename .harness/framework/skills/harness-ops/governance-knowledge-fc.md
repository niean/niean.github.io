---
name: governance-knowledge-fc
description: Use when a user asks to update .harness/knowledge from current repository code, audit stale knowledge docs against implementation, or treat code as source of truth for Harness knowledge.
---

# Skill: 从代码治理知识库

## 核心原则

代码是实现事实的第一真相；prd 是产品意图真相。代码与 knowledge 冲突时更新 knowledge，代码与 prd 冲突时提示用户，不自动改 prd。

## Step 1 -- 读取知识索引与目标范围

- 读取 .harness/PROJECT.md，确认知识库目录、知识回填文件映射、AI-READONLY 规则
- 读取 .harness/knowledge/ 全部文件首行 SUMMARY，建立目标索引
- 完整读取 .harness/knowledge/01-overview.md 和 .harness/knowledge/22-file-map.md
- 解析用户范围：默认扫描全部 .harness/knowledge/；若用户指定文件或主题，仅缩小代码审计范围，不跳过 Step 5 的同步 grep

## Step 2 -- 代码审计

按知识文件分工核对代码，必须给每个候选变更记录代码证据（file:line）：

| 目标知识 | 代码证据来源 |
|---|---|
| 01-overview.md | App 入口、AppState、主流程 |
| 02-architecture.md | UI/Core/Models 分层、模块边界、跨层调用 |
| 03-conventions.md | Constants、Logger、缓存、错误、测试、安全实现 |
| 04-data-boundaries.md | Models、Managers、Resources/config_example.json、磁盘结构 |
| 05-key-patterns.md | 跨文件协作流程、后台任务、传输、播放、图片加载 |
| 21-glossary.md | 类型定义、枚举、核心概念字段 |
| 22-file-map.md | 实际文件树、测试、资源、入口映射 |

禁止只用文件名推断；每条候选必须来自代码读取或 grep 证据。

## Step 3 -- 生成回填方案[CONFIRM]

输出并等待用户确认：

| # | 目标文件 | 当前知识 | 代码证据 | 建议变更 | 受影响引用 |
|---|---------|---------|---------|---------|-----------|

同时说明：
- 不确定项列为“需用户决策”，不写入 knowledge
- 涉及 prd/、framework/agents/、framework/guides/ 的修改只提议，不执行

## Step 4 -- 执行回填

按确认项修改 .harness/knowledge/ 文件：
- 保持原文件标题层级、列表风格和术语
- 用最小改动替换过期事实；新增内容放到最相关章节
- 文件映射新增路径前必须确认路径存在
- SUMMARY 只有在文件主题发生变化时才更新

## Step 5 -- 同步 grep 与一致性验证

必须 grep 所有变更前后实体名、关键旧表述、目标文件路径，范围包括：
`.harness/` 全部 .md、AGENTS.md、CLAUDE.md。

验证项：
- 旧过期表述 0 匹配，或仅剩历史计划/教训且明确说明不改
- 新增映射路径存在
- PROJECT.md 摘要与 knowledge 权威源不冲突
- prd 冲突已提示用户，不被 knowledge 静默覆盖

## 常见错误

| 错误 | 修正 |
|---|---|
| “赶时间，只修明显项” | 明显项也要代码证据、确认方案、grep 验证 |
| 只扫 22-file-map.md | 代码事实会影响架构、约定、数据边界、术语、关键模式 |
| 用 prd 覆盖代码事实 | prd 是意图；实现事实以代码为准，冲突需提示 |
| 新增文件映射不验路径 | 先确认路径存在，再写入 22-file-map.md |
| 修改 knowledge 后不查引用 | 必须 Step 5 全范围 grep |

## 输出摘要

报告：扫描的代码区域、修改的 knowledge 文件、同步检查结果、剩余需用户决策项、AI-READONLY 是否涉及。
