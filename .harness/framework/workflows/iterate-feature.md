---
name: iterate-feature
description: 功能迭代端到端工作流，编排 Designer/Planner/Coder/Reviewer 完成从需求到验收的全流程
---

# Workflow: 迭代功能

7 阶段混合编排：harness（知识库加载）-> superpowers（需求探索与设计 -> 计划 -> 实现）-> harness（验收 -> 知识回填 -> 总结）。

---

## 进度清单

执行时复制此清单追踪进度：

```
Workflow Progress:
- [ ] Phase 1: 知识加载（知识库加载、约束确认）
- [ ] Phase 2: 需求探索与设计（spec 落盘）[GATE]
- [ ] Phase 3: 计划制定（plan 落盘）[GATE-ENTRY]
- [ ] Phase 4: 代码实现（按 plan 逐 task）
- [ ] Phase 5: 结果验收（构建 + 扫描 + 验收标准）
- [ ] Phase 6: 知识回填
- [ ] Phase 7: 任务总结（归档 spec/plan）
```

---

## Phase 1: 知识加载
- Agent: Orchestrator
- 执行 `Skill: 加载知识库`（`.harness/framework/skills/harness/load-knowledge.md`），参数 task_type=feature, is_first_load=true
- 确认约束与产品方向

检查点：`[Phase 1 知识加载] 索引: N个文件, 必读: 已加载M个, 按需: K个可查阅`

## Phase 2: 需求探索与设计 `[GATE]`
- Agent: Designer
- 执行 `Skill: brainstorming`（`.harness/framework/skills/superpowers/brainstorming.md`），按其完整流程执行
- spec 落盘后，向用户输出需求摘要（目标 + 范围 + 方案 + 验收标准），等待确认
- 用户修正时：更新 spec，输出完整摘要再次确认
- `[GATE]` 规则见 FRAMEWORK.md

检查点：`[Phase 2 需求探索与设计] goal: ..., scope: N 文件, 方案: 已确认`

## Phase 3: 计划制定 `[GATE-ENTRY]`
- Agent: Planner
- `[GATE-ENTRY]` 前置条件：用户已在上一条消息中明确确认 spec；若 Phase 2 在当前回复中刚输出，说明 GATE 被违反，必须停止
- 执行 `Skill: writing-plans`（`.harness/framework/skills/superpowers/writing-plans.md`），按其流程执行到 "Plan Review Loop" 后终止；"Execution Handoff" 由本 Phase 自行执行
- plan 落盘后，确定执行方式（Subagent-Driven / Inline Execution）后直接进入 Phase 4：若用户在输入指令中明确指定了执行方式则遵从；否则 AI 按任务规模自主决策，plan 中 task <= 3 个时使用 Inline Execution，其余使用 Subagent-Driven，无需人工确认。禁止中断回复等待确认 -- 本 Phase 无 [GATE] 标记，plan 落盘后必须自主推进

检查点：`[Phase 3 计划制定] tasks: N 个, steps: M 步, 执行方式: subagent/inline`

## Phase 4: 代码实现
- Agent: Coder
- 执行 `Skill: subagent-driven-development`（`.harness/framework/skills/superpowers/subagent-driven-development.md`）或 `Skill: executing-plans`（`.harness/framework/skills/superpowers/executing-plans.md`），按 Phase 3 确定的执行方式选择；Subagent-Driven 模式可传入 model 参数，Inline Execution 始终使用主 Agent 模型

检查点：`[Phase 4 代码实现] 变更: file1(修改), file2(新增), ...; tasks: N/M 完成`

## Phase 5: 结果验收
- Agent: Reviewer，主 Agent 内联执行；可传入 model 参数指定扫描 subagent 使用的 LLM 模型
- 执行 `Skill: 结果验收`（`.harness/framework/skills/harness/verify-acceptance.md`），scope=full，传入变更文件列表和 spec 验收标准
- 错误、警告均视为不通过；不通过时回到 Phase 4 修复（反馈环路），Phase 4 -> Phase 5 的完整循环最多执行 3 轮（含首次），第 3 轮仍不通过时中断流程，向用户输出错误报告（未通过项 + 已尝试的修复方案），等待人工介入决策。用户介入后可选择：(a) 提供修复指导后从 Phase 4 继续（不重置轮次计数），(b) 接受当前状态结束任务，(c) 终止任务

检查点：`[Phase 5 结果验收] 构建: 通过/失败, 扫描: N维度/M违规, 验收标准: K项通过`

## Phase 6: 知识回填
- Agent: Orchestrator
- 执行 `Skill: 回填知识库`（`.harness/framework/skills/harness/backfill-knowledge.md`），增量模式
- 输入：Phase 4 变更文件列表 + Phase 2 spec 摘要（有变化才写，无变化也告知）

检查点：`[Phase 6 知识回填] 回填: N个文件, 状态: 有变化/无变化`

## Phase 7: 任务总结
- Agent: Orchestrator
- 执行顺序：`Skill: 归档任务文件`（输入：Phase 2 spec 文件路径 + Phase 3 plan 文件路径）-> `Skill: 总结任务` -> 结束任务，在同一条回复中完成

检查点：`[Phase 7 任务总结] 归档: spec+plan, 状态: 完成`

---

## 上下文管理

1. Phase 2 Designer 在主 Agent 上下文中执行（按 brainstorming Skill 流程交互）
2. Phase 3 后主动释放产品文档原文，按需时可重新读取 prd/ 文件；仅保留 spec + plan
3. Phase 4 按 plan 逐 task 加载必要源文件
4. Phase 5 扫描 subagent 有独立上下文
