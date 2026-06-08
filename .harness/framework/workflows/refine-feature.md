---
name: refine-feature
description: 精调功能端到端工作流，适用于小型、明确的简单需求/功能迭代，跳过设计和计划阶段，直接编码实现
---

# Workflow: 精调功能

3 阶段轻量编排：最小化知识加载 -> 直接编码实现 -> 编译通过。适用于需求明确、改动范围小的功能迭代，无需 spec/plan 文件落地。

---

## 进度清单

执行时复制此清单追踪进度：

```
Workflow Progress:
- [ ] Phase 1: 知识加载（最小化加载，仅文件映射等核心索引）
- [ ] Phase 2: 代码实现（直接编码，实现功能）
- [ ] Phase 3: 编译通过（build 零警告）
```

---

## Phase 1: 知识加载
- Agent: Orchestrator
- 执行 `Skill: 加载知识库`（`.harness/framework/skills/harness/load-knowledge.md`），参数 task_type=refine, is_first_load=true

检查点：`[Phase 1 知识加载] 索引: N个文件, 必读: 已加载M个, 按需: K个可查阅`

## Phase 2: 代码实现
- Agent: Orchestrator
- 直接编码实现功能，无需产出 spec 或 plan 文件
- 遵守 PROJECT.md 项目规范（编码约定、架构边界、质量守护、安全规范）
- 按需查阅 knowledge/ 中的文件（如涉及跨文件模式查阅 05-key-patterns.md）

检查点：`[Phase 2 代码实现] 目标: ..., 变更: file1(修改/新增), ...; 状态: 完成`

## Phase 3: 编译通过
- Agent: Orchestrator
- 执行 `Skill: 结果验收`（`.harness/framework/skills/harness/verify-acceptance.md`），scope=build_only
- 不通过时回到 Phase 2 修复（反馈环路），Phase 2 -> Phase 3 的完整循环最多执行 3 轮（含首次），第 3 轮仍不通过时中断流程，输出错误报告等待人工介入

检查点：`[Phase 3 编译通过] 构建: 通过/失败`

---

## 上下文管理

1. Phase 1 仅加载最小化知识（文件映射 + 项目概览），不加载完整架构/约定文档
2. Phase 2 按需查阅 knowledge/ 文件，不预加载
3. 无 spec/plan 文件生命周期管理
