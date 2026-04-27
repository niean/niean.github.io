# Skill: 治理全部

触发：人工指令。编排多个治理 Skill 按顺序执行。

本 Skill 采用多 Agent 编排（Orchestrator 调度），每个 Step 委托对应子 Skill 执行，子 Skill 架构以其自身定义为准。

输出规范：遵守 AGENTS.md "流程合规 > 消息输出格式"中定义的全部规则。

## 上下文管理

每步完成后输出检查点摘要（不超过 5 行），后续只携带摘要。每步只加载必需文件。所有步骤必选，禁止跳过；上下文紧张时先压缩再继续。

## 步骤

### Step 1 -- 治理代码
- Agent: Orchestrator 调度，委托 Skill: 治理代码（多 Agent 编排）
- 执行 `.harness/skills/governance-code.md`
- 摘要：`[Step 1 治理代码] 扫描N项违规，已修复M项，清理K个废弃项`

### Step 2 -- 治理技能
- Agent: Orchestrator 调度，委托 Skill: 治理技能（多 Agent 编排）
- 执行 `.harness/skills/governance-capability.md`
- 摘要：`[Step 2 治理技能] 修复N项，新增K个能力`

### Step 3 -- 回填知识库
- Agent: Orchestrator 调度，委托 Skill: 回填知识库（单 Agent）
- 执行 `.harness/skills/backfill-knowledge.md`
- 摘要：`[Step 3 回填知识库] agents/ 修正N处，AGENTS.md 更新M处`

### Step 4 -- 回填产品文档
- Agent: Orchestrator 调度，委托 Skill: 回填产品文档（单 Agent）
- 执行 `.harness/skills/backfill-prd.md`
- 摘要：`[Step 4 回填产品文档] baseline 更新N处，sense 更新M处`

### Step 5 -- 巡检报告
- Agent: Orchestrator
- 汇总 Step 1~4 摘要，输出巡检报告
