---
name: backfill-knowledge
description: 知识库回填，支持完整模式（全量扫描一致性）和增量模式（聚焦本次变更范围）
---

# Skill: 回填知识库

## 输入参数

| 参数 | 必需 | 说明 |
|------|------|------|
| mode | 否 | `incremental`（默认）增量模式，`full`完整模式 |
| changed_files | 增量模式必需 | 本次任务变更文件列表（来自 Phase 4 检查点） |
| task_summary | 增量模式必需 | 任务摘要（来自 spec/plan，含目标和范围） |


## 执行模式

### 增量模式（mode=incremental）

任务知识回填阶段自动调用。聚焦本次变更范围，按 .harness/PROJECT.md "知识回填文件映射" 回填 knowledge/，不扫描文档一致性，不等待人工确认。

按下方"增量模式步骤"执行。


### 完整模式（mode=full）

人工指令触发。全量扫描知识库与代码的一致性，含 .harness/framework/FRAMEWORK.md/、.harness/PROJECT.md 同步和人工确认。

按下方"完整模式步骤"执行。


---

## 增量模式步骤

### Step 1 -- 接收输入
从调用方获取 changed_files（变更文件列表）和 task_summary（任务摘要）。

### Step 2 -- 读取现状
- 读取 .harness/PROJECT.md "知识回填文件映射" 章节，确认回填映射关系
- 读取 `.harness/knowledge/` 全部文件首行 SUMMARY，建立索引
- 根据变更内容，完整读取可能需要更新的 knowledge 文件

### Step 3 -- 增量回填 knowledge/
对 changed_files 中每个文件执行：
1. 按 .harness/PROJECT.md "知识回填文件映射" 判断该文件是否触发回填条件
2. 触发则读取映射规则指定的目标 knowledge 文件并更新
3. 不触发则跳过

遍历结束后进入 Step 4

### Step 4 -- 输出回填摘要
有变化：列出具体变更（文件、变更内容）。无变化：告知"本次无需回填"。


---

## 完整模式步骤

### Step 1 -- 读取现状
读取 .harness/framework/FRAMEWORK.md + .harness/PROJECT.md + `.harness/knowledge/` 全部 + prd/ 目录结构 + `.harness/framework/skills/` 目录（含 subskills/），列出项目源码一级子目录（ls，不递归），对照 .harness/knowledge/02-architecture.md 确认模块划分一致。

### Step 2 -- 更新 knowledge/ 知识库
对比实际代码与文档：(1) 删除已不存在的文件/类型/函数引用，(2) 更新已变更的模块名/路径/接口签名，(3) 不重写未变更内容。

### Step 3 -- 提取 .harness/framework/FRAMEWORK.md、.harness/PROJECT.md 候选变更
识别：仓库结构不一致、Workflows/Skills 注册表过时、知识库索引不一致、.harness/PROJECT.md 摘要与 `.harness/knowledge/03-conventions.md` 不同步等。列出候选清单（位置、当前描述、建议描述、原因）。

### Step 4 -- 等待人工确认 `[CONFIRM]`
展示候选清单，结束当前回复，等待用户确认。

### Step 5 -- 更新 .harness/framework/FRAMEWORK.md、.harness/PROJECT.md
按确认项最小化修改。

### Step 6 -- 输出变更摘要