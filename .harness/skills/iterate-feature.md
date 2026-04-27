# Skill: 迭代功能

触发：人工下发功能需求或修改代码（新 Task 或同一 Task 内的第 2+ 次反馈）。

遵循 Global Workflow 6 阶段标准流程（`.harness/skills/global-workflow.md`）。

本 Skill 采用多 Agent 编排，每个 Phase 指定执行角色。Phase 间通过"检查点摘要"（不超过 10 行）交接上下文。

输出规范：遵守 AGENTS.md "流程合规 > 消息输出格式"中定义的全部规则。

---

## Phase 1: 任务调度
- Agent: Orchestrator
- 按 AGENTS.md "上下文管理"要求，首次加载必须读取 `.harness/context/` 全部文件（除 03-prd-specs.md）
- 确认约束与产品方向，启动 Phase 2

## Phase 2: 意图理解
- Agent: Analyst（subagent）
- 读取 `.harness/agents/analyst.md`，将需求填充到 `{user_request}`，通过 `use_subagents` 启动
- Analyst 按需读取知识库和产品文档，输出 spec（JSON）

检查点：`[Phase 2 意图理解] goal: ..., scope: N 文件, M 行为, K 验收标准`

## Phase 3: 意图确认 `[GATE]`
- Agent: Orchestrator
- spec 落盘到 `.harness/context/agents/agent-specs-${事项}.md`
- 向用户输出完整摘要（目标 + 影响范围 + 实现思路 + 验收标准），等待确认
- 用户修正时：重启 Analyst（`{correction}` 参数），更新 spec，输出完整摘要再次确认
- 用户修正 ≠ 用户确认：收到修正后必须重新输出完整摘要并重走 GATE 确认流程，禁止将修正视为确认直接进入 Phase 4
- `[GATE]` 每次输出完整摘要后（含修正后重新输出），必须使用 `ask_followup_question` 向用户请求确认，立即结束当前回复；禁止在同一条回复中继续 Phase 4

## Phase 4: 任务实现(含验收) `[GATE-ENTRY]`
- `[GATE-ENTRY]` 前置条件：用户已在上一条消息中明确确认 spec；若 Phase 3 在当前回复中刚输出，说明 GATE 被违反，必须停止

### Step 4.1: 代码实现
- Agent: Coder
- 读取 `.harness/agents/coder.md`，按 spec scope 加载源文件并实现
- 涉及核心模块变更时同步补充单元测试

### Step 4.2: 结果验收
- Agent: Reviewer，按 `.harness/agents/reviewer.md` Step 1-4 执行
- 扫描范围：仅本次变更文件
- 每个 Step 必须实际执行并产出独立结果，禁止跳过或虚报
- 构建失败、扫描违规或验收不通过时回到 Step 4.1

必须执行的步骤：
1. Step 1 构建验证：执行构建命令，要求零警告
2. Step 2 代码扫描：对变更文件执行多维度扫描，逐维度输出结论
3. Step 3 验收标准检查：对照 spec 验收标准逐项验证，输出每项通过/不通过
4. Step 4 测试验证：有相关测试时执行，无则标注"跳过"及原因

检查点：`[Phase 4 任务实现] 变更: file1(修改), file2(新增), ...; 构建: 通过/失败, 扫描: N维度/M违规, 验收标准: K项通过, 测试: 通过/跳过`

## Phase 5: 知识回填
- Agent: Orchestrator
- 按 AGENTS.md 知识回填规则回填 context/agents/（有变化才写，无变化也告知）
- `rm -f` 删除临时 spec

## Phase 6: 任务总结 `[GATE]`
- Agent: Orchestrator
- 自动触发 Skill: 总结任务（`.harness/skills/summarize-task.md`）
- 执行顺序：输出总结报告（通过 `ask_followup_question`）-> 用户确认收到 -> attempt_completion
- 总结报告与 attempt_completion 不得合并
- `[GATE]` 总结报告输出后，必须立即结束当前回复，等待用户确认收到；禁止在同一条回复中调用 `attempt_completion`

---

## 上下文管理

1. Phase 2 Analyst subagent 有独立上下文窗口
2. Phase 3 后仅保留 spec，不保留产品文档原文
3. Phase 4 只加载 spec + scope 内源文件
4. Step 4.2 扫描 subagent 有独立上下文
5. 上下文紧张时先压缩检查点摘要再继续
