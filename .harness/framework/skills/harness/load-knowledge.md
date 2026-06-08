---
name: load-knowledge
description: 分层加载知识库，按任务类型加载矩阵读取必读文件，支持首次加载和按需加载
---

# Skill: 加载知识库

## 输入参数

| 参数 | 必需 | 说明 |
|------|------|------|
| task_type | 是 | 任务类型：`feature`（功能需求）、`refine`（精调功能）、`bugfix`（Bug修复）、`governance`（治理/扫描）、`docs`（文档维护） |
| is_first_load | 否 | 是否首次加载（默认 true）；false 时跳过 Step 1 SUMMARY 索引，仅按需读取 |

## 执行步骤

### Step 1 -- 建立 SUMMARY 索引（is_first_load=true 时执行）

读取以下目录中每个 .md 文件的首行 `<!-- SUMMARY: ... -->` 注释，建立全局索引：
- `.harness/knowledge/` 全部文件
- `.harness/prd/`（除 `.harness/prd/03-prd-specs.md`）
- `.harness/framework/lessons/general.md`（Harness 通用教训）
- `.harness/lessons/project.md`（项目教训）

索引格式：文件名 -> SUMMARY 内容，供后续步骤和整个任务生命周期按需查阅。

### Step 2 -- 按加载矩阵完整读取必读文件

根据 任务类型（task_type） 查 .harness/PROJECT.md "任务类型加载矩阵"，完整读取对应"必读"列的文件。"按需读取"列的文件不在此步骤加载，由后续 Phase 根据需要自行读取。

加载矩阵的权威定义在 `.harness/PROJECT.md`。

### Step 3 -- 输出加载摘要

输出格式：

```
知识库加载完成：
- 索引: N 个文件（knowledge M + prd K + lessons J）
- 必读: 已加载 X 个文件（列出文件名）
- 按需: Y 个文件可按需查阅（列出文件名）
```
