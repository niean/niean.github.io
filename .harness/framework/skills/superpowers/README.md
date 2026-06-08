# Harness适配superpowers - 修改记录

## 约束
本文仅供自然人使用，未经人工确认、禁止AI修改。

## 用途
记录 Harness 对 superpowers 原版技能的定制化修改，用于后续 Follow superpowers 版本升级时的合并参考。

---

## 一、全局修改（适用于多个文件）

### 1.1 技能间引用路径重映射
- 原版：技能间使用相对路径引用（如 `./finishing-a-development-branch.md`）
- 定制：统一改为 `.harness/framework/skills/superpowers/` 前缀（如 `.harness/framework/skills/superpowers/finishing-a-development-branch.md`）
- 影响文件：brainstorming.md, writing-plans.md, executing-plans.md, subagent-driven-development.md, systematic-debugging.md, writing-skills.md, requesting-code-review.md

### 1.2 Phase N 重命名为 P N
- 原版：superpowers 内部阶段使用 `Phase N` 命名
- 定制：统一改为 `P N`，避免与 Harness Skill 流程的 `Phase N` 命名冲突
- 影响文件：systematic-debugging.md, using-git-worktrees.md

### 1.3 Task N 重命名为 T N
- 原版：superpowers 内部任务使用 `Task N` 命名
- 定制：统一改为 `T N`，避免与 Harness 的 `Task` 命名冲突
- 影响文件：subagent-driven-development.md, requesting-code-review.md

### 1.4 Step N 重命名为 S N
- 原版：superpowers 内部步骤使用 `Step N` 命名
- 定制：统一改为 `S N`，避免与 Harness Skill 流程的 `Step N` 命名冲突
- 影响文件：writing-plans.md, finishing-a-development-branch.md, executing-plans.md, systematic-debugging.md, writing-skills/anthropic-best-practices.md

### 1.5 AGENTS.md 调用约束
- 在 AGENTS.md 中添加：禁止主动调起 superpowers 插件（形如 `superpowers:skill-x`），仅在用户明确指令时才可调用
- 这是 Harness 层面的约束，不修改 superpowers 文件本身

---

## 二、逐文件修改

### 2.1 brainstorming.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| Checklist S 5 | 写 spec 到通用路径 | 写 spec 到 `.harness/specs/active/spec-{YYMMDD}-{desc}.md` | 对接 Harness 执行计划管理 |
| After the Design | 同上 | 同上 | |
| Spec document template | 英文字段（Created, Status, Source） | 中文字段（创建时间, 状态, 任务来源） | 模板本地化 |
| Spec document template | 英文章节名 | 中文章节备注（涉及数据结构变更时、涉及界面变更时） | |
| After the Design | "Commit the design document to git" | 已删除 | 不执行 git commit |
| User Review Gate | "Spec written and committed to" | 改为 "Spec written to" | 移除 committed 措辞 |
| User Review Gate | 完整 User Review Gate 节 | 已删除 | 用户确认由调用方接管 |
| Implementation | "Invoke the writing-plans skill" | 已删除 | 技能间流转由调用方接管 |
| Checklist S 7-8 | User reviews spec + Transition to implementation | 已删除 | 同上 |
| Process Flow 流程图 | 含 "User reviews spec?" + "Invoke writing-plans skill" | 终止于 "Spec written" | 流程图截止到 spec 完成 |
| terminal state 说明 | "The terminal state is invoking writing-plans" | 改为 "The caller decides how to proceed" | |
| 未迁移标记 | N/A | `<!-- not migrated: elements-of-style skill -->` | 原版子技能未引入 |

### 2.2 writing-plans.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| Save plans to | 通用路径 | `.harness/plans/active/plan-{YYMMDD}-{desc}.md` | 对接 Harness 执行计划管理 |
| Plan Document Header | 英文字段 | 中文字段（创建时间, 状态, 关联 spec） | 模板本地化 |
| Plan Document Footer | 原版无此节 | 新增变更记录表 + 技术债追踪（引用 debt-tracker.md） | Harness 新增，用于任务追踪 |
| Footer 说明段落 | 原版无 | 新增中文说明段落（任务执行中更新...） | |

### 2.3 requesting-code-review.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| PLAN_OR_REQUIREMENTS 示例 | 通用路径 | `.harness/plans/active/plan-{YYMMDD}-{desc}.md` | 路径重映射 |

### 2.4 brainstorming/spec-document-reviewer-prompt.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| Dispatch after | 通用路径 | `.harness/specs/active/` | |

### 2.5 writing-plans.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| Overview | "Frequent commits" | 已删除 | 不执行 git commit |
| Context | "should be run in a dedicated worktree" | 已删除 | 不使用 worktree |
| Bite-Sized Task | "Commit" - step | 已删除 | 不执行 git commit |
| Task Structure | S 5: Commit 模板 | 已删除 | 不执行 git commit |
| Remember | "frequent commits" | 已删除 | |
| Plan Review Loop | "proceed to execution handoff" | 改为 "plan is ready" | |
| Execution Handoff | 整节（auto-selection + Subagent/Inline 引用） | 已删除 | 执行方式由调用方决定 |

### 2.6 executing-plans.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| Remember | "Never start on main/master without explicit user consent" | 已删除 | 分支管理由调用方控制 |
| S 3 | finishing-a-development-branch REQUIRED | 改为"调用方决定收尾流程" | 收尾由 iterate-feature P5-7 接管 |
| Integration | using-git-worktrees REQUIRED + finishing REQUIRED | 仅保留 writing-plans 引用 | worktree/finishing 已移除 |

### 2.7 subagent-driven-development.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| 流程图+示例 | "implements, tests, commits, self-reviews" | 移除 "commits"/"Committed" | 不执行 git commit |
| Red Flags | "Never start on main/master without explicit user consent" | 已删除 | 分支管理由调用方控制 |
| Integration | using-git-worktrees REQUIRED + finishing REQUIRED | 仅保留 writing-plans + requesting-code-review | worktree/finishing 已移除 |
| 末尾流程图 | finishing-a-development-branch | 改为 "Announce completion" | 收尾由调用方接管 |
| [FINAL_REVIEW_STEP] | 流程图节点 + 示例中的 FINAL_REVIEW_STEP | 已删除 | review 由调用方接管 |
| When to Use 与 The Process 之间 | 原版无此节 | 新增 Input Parameters 节（model 可选参数） | 支持调用方传入 model 覆盖 Model Selection 策略 |

### 2.8 implementer-prompt.md

| 位置 | 原版 | 定制 | 说明 |
|------|------|------|------|
| Your Job | S 4: [COMMIT_STEP] + 占位符说明 | 已删除，步骤重编号 | 不执行 git commit |

### 2.9 未修改文件（保持原版）

以下文件未发现定制化修改（除全局路径重映射外）：

- using-superpowers.md
- test-driven-development.md
- test-driven-development/testing-anti-patterns.md
- verification-before-completion.md
- receiving-code-review.md
- dispatching-parallel-agents.md
- finishing-a-development-branch.md
- systematic-debugging/root-cause-tracing.md
- systematic-debugging/defense-in-depth.md
- systematic-debugging/condition-based-waiting.md
- writing-skills/anthropic-best-practices.md
- writing-skills/graphviz-conventions.dot
- writing-skills/render-graphs.js
- writing-skills/persuasion-principles.md
- writing-skills/testing-skills-with-subagents.md

---

## 三、未迁移内容汇总

原版 superpowers 中存在但未引入本项目的子技能/资源：

| 原版资源 | 引用位置 | 说明 |
|----------|---------|------|
| elements-of-style skill | brainstorming.md | 写作风格指南（独立插件，非 superpowers 内置） |

---

## 四、升级操作指南

superpowers 版本升级时，按以下步骤合并：

1. 对比原版 diff，识别新增/修改的文件
2. 对照本文"逐文件修改"表格，保留定制化内容（路径、模板、Footer 等）
3. 检查"未迁移内容"是否有需要新引入的子技能
4. 更新本文档，记录新版本引入的变更

