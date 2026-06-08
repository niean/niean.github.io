# FRAMEWORK.md -- Harness Framework

通用能力规范，项目无关，跨项目共享。

---

# 一、任务调度（任务入口）

本节是`任务调度`的实际执行者，由 Agent:Orchestrator 承担。

任务开始时，首先且必须执行`任务调度`(禁止跳过)：判断任务类型，按顺序优先匹配下表：

| 任务类型 | 触发条件 | 编排流程 |
|---------|---------|---------|
| Slash Command | 用户通过 slash command 触发 | 直接执行 |
| 显式指定 | 用户明确指定已注册 Workflow/Skill 名称（含治理类 Workflow） | 直接路由到对应 Workflow/Skill |
| 功能迭代 | 人工下发功能需求或修改代码 | Workflow: 迭代功能 |
| 功能精调 | 人工下发简单需求或功能精调 | Workflow: 精调功能 |
| Bug修复 | Bug修复或异常行为修复 | Workflow: 修复Bug |
| 文档修改 | 修改文档需求 | Workflow: 迭代文档 |
| 其他 | 以上均未匹配 | 直接执行 |

任务调度约束：
- Workflow 优先级高于独立Skill，独立Skill 禁止主动拦截 Workflow 入口；
- superpowers:xxx(平台插件) 严禁主动调起，仅在用户明确指令时调用；与 `.harness/framework/skills/superpowers/` 下被 Workflow 声明依赖的本地 Skill 无关
- 直接调用的 Skill 如有前置上下文依赖（如变更文件列表、设计文档），由 Skill 自身检查并提示用户补充

---

# 二、执行约束

## Workflow 执行

1. 读取定义：立即读取对应的 Workflow 文件（如 `.harness/framework/workflows/iterate-feature.md`）
2. 按 Phase 顺序执行：不跳过、不简化、不改编、不拆分、不合并
3. 遵守 `[GATE]` 门禁（见下方 GATE 规则），在 GATE 点等待用户确认后再继续
4. 按 Phase 定义的消息输出格式输出，不简化、不改动

## Skill 执行

1. 读取定义：立即读取对应的 Skill 文件（如 `.harness/framework/skills/harness/load-knowledge.md`）
2. 按 Step 顺序连续执行；默认无中断，Skill 可通过 `[CONFIRM]` 标记声明人工确认点（结束当前回复，等待用户确认后继续）；必须先读取定义，再开始实现

## Phase 门禁（GATE）规则

GATE 管控 Phase 间流转，不管控 Phase 内部操作。Phase 内部的确认（如 AI-READONLY 文件逐个确认）由各自规则约束，不受 GATE 规则限制。

- `[GATE]` 标记的 Phase 结束后，必须立即结束当前回复，等待用户下一条消息明确确认；禁止在同一条回复中继续后续 Phase
- `[GATE]` Phase 收到用户修正时：更新内容后必须重新输出完整摘要并重走 GATE 确认流程；用户修正 ≠ 用户确认，禁止将修正视为确认直接进入后续 Phase
- `[GATE-ENTRY]` 标记的 Phase 开始前，必须执行前置条件检查：(1) 上一条用户消息包含明确确认（如"确认""Yes""ok""继续"等），(2) 前置 GATE Phase 不在当前回复中输出。任一条件不满足则停止并提示用户
- GATE 点以各 Workflow 文件中标注的 `[GATE]` / `[GATE-ENTRY]` 为准，AGENTS.md 不维护硬编码列表
- 非 GATE Phase 禁止因 Phase 间流转而中断回复等待用户确认；AI 应按 Workflow 定义自主推进到下一 Phase

## 消息输出格式

任务开始时声明类型和架构，每个 Phase 使用标题 + 角色标注 + 正文的三行结构。格式如下：

```
任务类型：功能需求；调度架构：多Agent

## Phase 1: 知识加载
[Agent: Orchestrator]
正文内容...

## Phase 4: 代码审查
[Agent: Reviewer (subagent)]
正文内容...
```

- 同一 Task 内第 2+ 次迭代，声明追加：`同一 Task 内第 N 次迭代`
- Phase 标题使用 Workflow 文件中定义的 Phase 名称；Phase 内调用 Skill 时，使用 Skill 注册表中的显示名
- 约束类术语（"硬性门禁""流程违规"等）不输出到用户消息框

## 受保护章节规则

- AI 不得自动修改 AI-READONLY 内容；AI 发现问题时只能以消息方式提示用户，不得主动发起修改请求
- 用户主动发起的 Workflow/Skill 中，AI-READONLY 文件的每次修改需逐个获得用户明确确认后方可执行

---

# 三、通用规范

## Agents（角色 Agent）

Agent 定义"谁来做"，Workflow 编排"按什么顺序做"，Skill 提供"原子能力"。Workflow 的每个 Phase 指定执行 Agent，Phase 间通过"检查点摘要"（不超过 10 行）交接上下文。详细定义见 `.harness/framework/agents/` 目录。

| Agent | 运行形态 | 模板文件 | 职责 |
|-------|---------|---------|------|
| Orchestrator | 主 Agent | .harness/framework/agents/orchestrator.md | 任务路由、流程编排、上下文管理 |
| Designer | 主 Agent | .harness/framework/agents/designer.md | 需求探索、方案设计、spec 产出 |
| Planner | 主 Agent | .harness/framework/agents/planner.md | 计划拆分、plan 产出 |
| Coder | subagent + 主 Agent | .harness/framework/agents/coder.md | 代码实现 |
| Reviewer | subagent + 主 Agent | .harness/framework/agents/reviewer.md | 代码扫描、构建验证、验收 |

subagent 为性能优化手段，非流程成败条件。所有使用 subagent 的 Phase/Skill 必须支持主 Agent 顺序执行的降级路径，降级不改变产出质量要求。

## Workflows（端到端编排）

编排多个 Agent 角色完成端到端目标，含 GATE 门禁和反馈环路。详细定义见 `.harness/framework/workflows/` 目录。

| Workflow | 文件 |
|----------|------|
| 迭代功能 | .harness/framework/workflows/iterate-feature.md |
| 精调功能 | .harness/framework/workflows/refine-feature.md |
| 修复Bug | .harness/framework/workflows/fix-bug.md |
| 迭代文档 | .harness/framework/workflows/iterate-docs.md |
| 治理代码-人工 | .harness/framework/workflows/harness-ops/governance-code-manual.md |
| 治理技能-人工 | .harness/framework/workflows/harness-ops/governance-capability-manual.md |


## Skills（可复用操作）

Skill 只定义"做什么"和"怎么做"，不声明自身的触发时机；调用时机由 Workflow/Orchestrator 决定。触发后读取对应文件、按步骤执行。详细定义见 `.harness/framework/skills/` 目录。

| Skill | 调用场景 | 文件 |
|-------|------|------|
| 加载知识库 | Workflow显式调用，或人工指令 | .harness/framework/skills/harness/load-knowledge.md |
| 回填知识库 | Workflow显式调用，或人工指令 | .harness/framework/skills/harness/backfill-knowledge.md |
| 归档任务文件 | Workflow显式调用，或人工指令 | .harness/framework/skills/harness/archive-task-files.md |
| 从教训回填知识库 | 人工指令 | .harness/framework/skills/harness-ops/backfill-knowledge-fl.md |
| 从代码治理知识库 | 人工指令 | .harness/framework/skills/harness-ops/governance-knowledge-fc.md |
| 回填产品文档 | 人工指令 | .harness/framework/skills/harness-ops/backfill-prd.md |
| 结果验收 | 功能迭代或Bug修复完成后自动执行，或人工指令 | .harness/framework/skills/harness/verify-acceptance.md |
| 提取Harness模板 | 人工指令 | .harness/framework/skills/harness-ops/extract-harness-tpl/SKILL.md |
| 扫描Harness文档 | 人工指令 | .harness/framework/skills/harness-ops/scan-harness.md |
| 总结任务 | Workflow显式调用 | .harness/framework/skills/harness/summarize-task.md |


### 外部依赖能力

平台提供的能力，项目不维护其定义，Workflow 中按文件路径直接引用。

| 来源 | 目录 | 性质 | 调用约束 |
|------|------|------|---------|
| superpowers 插件 | .harness/framework/skills/superpowers/ | 平台提供，随平台演进 | 仅在用户明确指令时调用，不主动调起；Workflow 可声明依赖 |

## 文件与文档

- 禁止主动创建 README；禁止自主删除项目文件，治理/升级等场景允许经用户确认后删除
- 文件名：小写英文 kebab-case，动词-名词 语序（如 governance-code）；标题和描述使用中文，同样动词-名词 语序
- 命名语言约定：Agent 名称使用英文（Orchestrator、Reviewer）；Skill/Subskill 显示名使用中文（迭代功能、扫描架构边界）、文件名使用英文 kebab-case；消息输出中角色标注使用英文（`[Agent: Orchestrator]`）
- 阶段命名规范：Workflow 阶段称 Phase，Skill 阶段称 Step，其它称 Todo；引用外部依赖时简写为 P/S/T
- AI 只读目录（修改前必须人工确认）：.harness/framework/agents/、.harness/prd/、.harness/framework/guides/
- prd/ 与 knowledge/ 知识库冲突时，以 prd/ 为准（产品文档优先），同时提示用户确认是否需要更新 knowledge/ 对应内容
- 文档禁用 emoji/加粗/斜体，使用普通文字
- 执行计划文件管理详见"执行计划管理"章节
- 引用方向自上而下，下层不反向引用上层具体定义（详见 .harness/framework/guides/00-harness-desc.md 3.3 节）
- .harness/ 下引用项目文件路径时，使用项目根目录相对路径，不使用绝对路径

## 命令执行

- 多步命令组合（3+ 条独立命令串联，或总行数超过 10 行）时，必须先将脚本写入 `locals/harness_tmp/` 再执行，防止 Terminal 异常阻塞流程
- `locals/harness_tmp/` 由 AI 自主维护（创建、清理均无需用户确认），已在 `.gitignore` 覆盖范围内

## 上下文管理

- 首次加载（Task 首条消息）分层加载知识库：
  1. 必读：读取 PROJECT.md "知识库目录"声明的所有目录，每个 .md 文件的首行 `<!-- SUMMARY: ... -->` 注释，建立全局索引
  2. 必读：完整读取项目概览文档 + 文件映射文档
  3. 按需：根据任务类型完整读取相关文件（见 PROJECT.md "任务类型加载矩阵"）
- 后续迭代（同一 Task 内），按需查阅知识库目录下文件，不重复加载已知内容，因为每类知识有且只有一个归属文档、不重复维护
- 多步任务：每步完成压缩为检查点摘要（见下方"检查点摘要模板"），后续只携带摘要；每步只加载必需文件
- 所有步骤均为必选项，禁止因上下文压力跳过；上下文不足时先压缩检查点摘要（每条单行）再继续
- 委派产出（subagent、跨 Phase 交接）：产出结构化结论（表格、要点），不搬运原文；需要完整内容时直接读取源文件
- 产出超限时：在检查点摘要中标记当前 Phase 状态为"部分完成"，列出未完成步骤编号和名称，在下一条回复中从未完成步骤继续；不重试相同范围
- 各 Skill 如有更具体的上下文管理要求，以 Skill 文件为准

### 检查点摘要模板

Phase 间交接使用结构化检查点摘要，每条摘要为单行，整个交接区累计不超过 10 行。标准格式：

```
[Phase N: 名称] 目标: {一句话}; 产出: {文件/决策}; 变更: {file1(修改), file2(新增)}; 状态: {完成/部分完成}; 后续依赖: {下一Phase需要的关键信息}
```

各 Skill 可在此模板基础上定义更具体的字段（如 iterate-feature 的 scope/tasks 字段），但每条摘要必须保持单行格式。

## 执行计划管理

AI 通过 `.harness/specs/` 和 `.harness/plans/` 自主管理设计文档和实现计划（目录结构见"仓库结构"）。

### Spec 与 Plan

- Spec 命名：`spec-{YYMMDD}-{desc}.md`，模板见 `.harness/framework/skills/superpowers/brainstorming.md`
- Plan 命名：`plan-{YYMMDD}-{desc}.md`，模板见 `.harness/framework/skills/superpowers/writing-plans.md`
- Spec 触发：默认必须产出 spec；用户显式要求跳过、或指令显式要求跳过时，可省略 spec
- Spec 是一次性产物，实现完成后持久性知识通过 Phase 5 回填 knowledge/
- 同一窗口内第 2+ 次迭代复用同一计划文件

### 生命周期

同一 Task 允许 1 spec + 1 plan；不同 Task 的文件可在 active/ 中并行。

| 阶段 | 操作 | 规则 |
|------|------|------|
| Phase 1 知识加载 | 检测 active/ | 按文件名日期和描述匹配当前任务，匹配则复用；不匹配视为其他 Task 文件，后续 Phase 新建。completed/ 中有匹配则移回 active/ 复用；均无则后续 Phase 创建 |
| Phase 2 需求探索 | 写入 spec | spec -> `specs/active/`（仅迭代功能） |
| Phase 3 计划制定 | 写入 plan | plan -> `plans/active/`（仅迭代功能） |
| 任务执行中 | 更新 plan | 更新检查清单、记录变更和技术债 |
| 任务总结 | 归档 | 状态改 completed，移到 `completed/` |

### 技术债管理

- 新引入的技术债必须在本次任务中解决，禁止拖延
- 新发现的技术债必须立即写入 `plans/debt-tracker.md`（获得 ID），有 plan 时在计划文件中引用该 ID；无 plan 场景（fix-bug/精调功能/治理/文档）来源计划填 N/A
- 格式：表格（ID/描述/优先级/来源计划/发现时间/状态）

## 知识回填规则

知识回填目标映射见 .harness/PROJECT.md "知识回填文件映射"。

## 教训库维护规则

AI 自主维护教训库，人工可通过提示或建议触发新增/修正。
教训是原始素材，knowledge/ 是提炼后的权威知识；教训通过人工触发的回填流程沉淀为知识。

- 写入时机：Bug修复完成后，根因需追踪 2+ 个源文件或跨越 PROJECT.md 架构知识文件中定义的架构分层才能定位时，自动提取教训写入；功能迭代中，实现方式与最初假设不同、导致代码回退或方案变更时，同样提取教训写入
- 分级：仅与 Harness 框架相关、不绑定具体语言/框架/项目的通用经验 -> 通用教训文件；绑定本项目的具体经验 -> 项目教训文件（具体路径见 PROJECT.md "教训库加载路径"）
- 条目格式：`### L/P{序号}: 标题`，含现象/根因/教训/来源四字段
- 编号：general 用 L001 递增，project 用 P001 递增
- 去重：写入前检查是否已有根因相同的教训条目，有则合并更新（追加新现象或补充教训），而非新增条目
- 加载策略：任务启动只读 SUMMARY 索引，不完整加载；仅用户明确指令或当前根因的关键词（错误类型、模块名、API名）在 SUMMARY 中出现时，读取对应教训详情
- 回填：人工触发 `Skill: 回填知识库` 时，将已沉淀的教训抽象为通用规则写入 knowledge/，回填后删除原教训条目
- 提取：`Skill: 提取Harness模板` 时 general.md 随模板带走，project.md 留在项目内

## 维护

修改约束/规范/规则时，检查 .harness/framework/FRAMEWORK.md 和 .harness/PROJECT.md 全局描述确保无矛盾。Agent 因缺少说明出错时：补充到 `.harness/knowledge/`，适用于所有项目（不绑定特定语言/框架/业务逻辑）的约束摘录到本文件，更新下方知识库索引。

## Framework 目录结构

```
.harness/framework/
  FRAMEWORK.md         -- 通用规范入口（本文件）
  agents/              -- Agent 角色模板（Orchestrator、Designer、Planner、Coder、Reviewer）
  workflows/           -- Workflow 端到端编排（迭代功能、修复Bug、迭代文档）
    harness-ops/       -- Harness 运维类 Workflow（治理代码-人工、治理技能-人工）
  skills/              -- Skill 定义
    harness/           -- Harness 核心 Skill
      subskills/       -- Subskill 扫描模板
    harness-ops/       -- Harness 运维类 Skill
    superpowers/       -- superpowers 方法论技能（开发方法论，本地适配版）
  guides/              -- 方法论与参考文档（人工维护）
  lessons/
    general.md         -- Harness 通用教训（AI自主维护）
```

## 通用知识索引

| 文件 | 何时查阅 |
|------|---------|
| .harness/framework/guides/00-harness-desc.md | 了解 Harness 体系描述时 |
| .harness/framework/guides/02-harness-dev.md | 了解 Harness 开发流程时 |
| .harness/framework/lessons/general.md | 用户指令或当前根因与 SUMMARY 高度相关时按需读取 |

注意：00-harness-desc.md 与 FRAMEWORK.md 有内容重叠（能力模型、阶段命名等），AI 已从 FRAMEWORK.md 获取执行规则时无需再读 00-harness-desc.md，除非用户明确要求。
