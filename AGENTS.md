# AGENTS.md -- niean's blog

聂安的个人博客

---

# 一、通用规范（项目无关）

## Agents（角色 Agent）

Skill 定义"做什么"，Agent 定义"谁来做"。多 Agent Skill 的每个 Phase 指定执行角色，Phase 间通过"检查点摘要"（不超过 10 行）交接上下文。详细定义见 `.harness/agents/` 目录。

| Agent | 运行形态 | 模板文件 | 职责 |
|-------|---------|---------|------|
| Orchestrator | 主 Agent | .harness/agents/orchestrator.md | 任务路由、流程编排、上下文管理 |
| Analyst | subagent（只读） | .harness/agents/analyst.md | 需求理解、结构化 spec 输出 |
| Coder | 主 Agent（实现阶段） | .harness/agents/coder.md | 代码实现 |
| Reviewer | subagent + 主 Agent | .harness/agents/reviewer.md | 代码扫描、构建验证、验收 |

## Skills（可复用操作）

触发后读取对应文件、按步骤执行。详细定义见 `.harness/skills/` 目录。

| Skill | 触发 | 文件 |
|-------|------|------|
| Global Workflow | 迭代类 Skill 自动遵循 | .harness/skills/global-workflow.md |
| 迭代功能 | 人工下发功能需求或修改代码 | .harness/skills/iterate-feature.md |
| 迭代其它 | 人工下发非代码类任务 | .harness/skills/iterate-other.md |
| 回填知识库 | 人工指令 | .harness/skills/backfill-knowledge.md |
| 回填产品文档 | 人工指令 | .harness/skills/backfill-prd.md |
| 治理代码 | 人工指令 | .harness/skills/governance-code.md |
| 验证构建 | 功能迭代完成后自动执行，或人工指令 | .harness/skills/verify-build.md |
| 治理技能 | 人工指令 | .harness/skills/governance-capability.md |
| 提取Harness模板 | 人工指令 | .harness/skills/extract-harness-tpl.md |
| 治理全部 | 人工指令 | .harness/skills/governance-all.md |
| 总结任务 | AI自动触发（任务完成后） | .harness/skills/summarize-task.md |

自动触发：标注"AI自动触发"的 Skill 必须在对应时机自动执行。当前仅 Skill: 总结任务（仅适用于按迭代功能或迭代其它完整流程执行的任务）。

## Subskills（并行扫描任务）

本项目暂不配置Subskills。

## Global Workflow（全局工作流）

如未明确规定，全局工作流必须采用 6 阶段标准流程，权威定义见 `.harness/skills/global-workflow.md`。

| 阶段 | 名称 | GATE | 语义 |
|------|------|------|------|
| 1 | 任务分解 | - | 读取约束、确认方向、识别任务类型、路由到具体 Skill |
| 2 | 意图识别 | - | 分析需求、产出结构化 spec |
| 3 | 意图确认 | [GATE] | spec 落盘、用户确认、修正循环 |
| 4 | 任务实现(含验收) | [GATE-ENTRY] | 按 spec 执行实现 + 对照验收标准检查 |
| 5 | 知识回填 | - | 回填 context/agents/ + 删除临时 spec |
| 6 | 任务总结 | [GATE] | 触发总结任务 -> 用户确认 -> 完成 |


## 流程合规

### 任务执行入口（不可压缩）

任务开始时首先进行 任务分类和Skill路由（新 Task 或同一 Task 内的第 2+ 次反馈均需分类），必须立即执行以下步骤，禁止跳过：

1. 任务分类：判断任务类型。优先匹配：用户明确指定已注册 Skill 名称（如"治理代码"等）时，直接路由到对应 Skill，跳过步骤 2-4。否则分为 3 大类：功能需求、修改代码、其它任务
2. Skill路由：功能需求或修改代码 -> `Skill: 迭代功能`，其它任务 -> `Skill: 迭代其它`
3. 读取 Skill 定义：根据任务类型，立即读取对应的 Skill 文件（`.harness/skills/iterate-feature.md` 或 `.harness/skills/iterate-other.md`）
4. 遵循 Skill 流程：按 Skill 文件定义的 Phase 顺序执行；特别强调，`Phase 3：意图确认`必须在消息框展示意图、等待人工确认，否则禁止执行 `Phase 4`

禁止行为：
- 禁止在读取 Skill 定义前直接开始代码实现
- 禁止跳过任何 Phase，禁止简化、改编、拆分或合并 Phase
- 禁止跳过`Phase 门禁[GATE]`（见下方 GATE 规则）
- 禁止跳过、简化、改动 Phase的消息输出格式


### Phase 门禁（GATE）规则（不可压缩）

- `[GATE]` 标记的 Phase 结束后，必须立即结束当前回复，使用 `ask_followup_question` 工具向用户请求确认；禁止在同一条回复中继续后续 Phase
- `[GATE]` Phase 收到用户修正时：更新内容后必须重新输出完整摘要并重走 GATE 确认流程；用户修正 ≠ 用户确认，禁止将修正视为确认直接进入后续 Phase
- `[GATE-ENTRY]` 标记的 Phase 开始前，必须确认用户已在上一条消息中给出明确回复；若前置 GATE Phase 在当前回复中刚输出，说明 GATE 被违反，必须停止
- 当前 GATE 点：迭代功能 Phase 3 -> Phase 4、迭代其它 Phase 3 -> Phase 4、迭代功能 Phase 6（总结 -> 完成）、迭代其它 Phase 6（总结 -> 完成）

### 引用外部步骤的执行约束（不可压缩）

- 当文档引用其它能力的 Step 而未展开描述时，在引用处必须附加约束：`每个 Step 必须实际执行并产出独立结果，禁止跳过或虚报`

### 不可压缩章节保护规则（不可压缩）

- 标记为 `不可压缩` 的章节，AI 发现其内容存在问题时，只能以消息方式提示用户
- AI 禁止自动修改 `不可压缩` 章节的内容
- AI 禁止索要用户确认然后代为修改 `不可压缩` 章节的内容（防止用户误授权）

### 消息输出格式（不可压缩）

- 任务声明：任务开始时声明任务类型和架构（新 Task 或同一 Task 内的第 2+ 次反馈均需声明），标准格式：`任务类型：功能需求；调度架构：多Agent` 或 `任务类型：修改文档；调度架构：单Agent`；同一 Task 内第 2+ 次反馈追加标注：`任务类型：功能需求；调度架构：多Agent。同一 Task 内第 N 次反馈`；非迭代功能类任务标注实际类型即可
- 阶段描述：Skill 流程中的每个 Phase，输出时使用 `## Phase N: 名称` 作为段落标题，名称严格对齐 Skill 定义（如 `## Phase 1: 任务调度`）；Phase 标题必须独占一行，禁止在同一行附加角色标注或其它内容
- 角色标注：每个 Phase/Step 输出标注执行 Agent：`[Agent: 角色名]` 或 `[Agent: 角色名 (subagent)]`，角色名使用英文；角色标注紧跟 Phase 标题下一行，不与标题混合
  - 阶段和角色组合格式示例：`## Phase 1: 任务调度`（标题独占一行）换行后 `[Agent: Orchestrator]`（角色标注独占一行）换行后正文内容
- 术语禁忌：约束类术语（"硬性门禁""流程违规"等）只在规范文档中体现，不输出到用户消息框

## 文件与文档

- 禁止主动创建 README；不删除项目文件（临时 spec `agent-specs-*.md` 除外，任务结束 `rm -f` 删除）
- 文件名：小写英文 kebab-case，动词-名词 语序（如 governance-code）；标题和描述使用中文，同样动词-名词 语序
- AI 只读目录（修改前必须人工确认）：.harness/agents/、.harness/context/users/、.harness/guides/
- users/ 与 agents/ 知识库冲突时，提示用户确认
- 文档禁用 emoji/加粗/斜体，使用普通文字
- 临时 spec 落盘到 `.harness/context/agents/agent-specs-${事项}.md`，仅供单次迭代，任务结束必须删除


### 文档引用方向

.harness/ 文档体系分为四层，引用方向应自上而下：

| 层级 | 目录 | 职责 |
|------|------|------|
| Layer 0 | AGENTS.md | 顶层入口，注册并索引所有 .harness/ 文件 |
| Layer 1 | .harness/agents/ | Agent 角色定义 -- "谁来做" |
| Layer 2 | .harness/skills/ | Skill 流程定义 -- "怎么做" |
| Layer 3 | .harness/skills/subskills/ | Subskill 任务模板 -- "做什么" |
| 数据层 | .harness/context/ + .harness/guides/ | 知识库、产品文档、方法论，被上层按需读取 |

引用方向规则：
- 向下引用：上层引用下层的具体定义（如 Skills 引用 Agents，Agents 调度 Subskills）
- 同层编排：同层文件可通过编排引用（如 governance-all.md 编排其他 Skills）
- 反向指回（限定）：下层仅允许"指回入口"式引用，不反向引用上层的具体定义

允许的特例：
- AGENTS.md 与 context/agents/03-conventions.md：双向声明摘要-权威源关系（AGENTS.md 项目规范为摘要，03-conventions.md 为权威源）
- context/agents/01-overview.md 指回 AGENTS.md：入口指引（"操作约束见 AGENTS.md"）

路径规则：
- .harness/ 下的文档引用项目文件路径时，使用项目根目录相对路径，不使用绝对路径

## 上下文管理

- 首次加载（Task 首条消息），必须读取 `.harness/context/` 全部文件（除 03-prd-specs.md），了解项目全貌
- 后续迭代（同一 Task 内），按需查阅 `.harness/context/`，不重复加载已知内容，因为每类知识有且只有一个归属文档、不重复维护
- 多步任务：每步完成压缩为检查点摘要（不超过 5 行），后续只携带摘要；每步只加载必需文件
- 所有步骤均为必选项，禁止因上下文压力跳过；上下文紧张时先压缩已有内容再继续
- 委派产出（subagent、跨 Phase 交接）：产出结构化结论（表格、要点），不搬运原文；需要完整内容时直接读取源文件
- 产出超限时：缩小单次任务范围或拆分为多个子任务，不重试相同范围
- 各 Skill 如有更具体的上下文管理要求，以 Skill 文件为准

## 维护

修改约束/规范/规则时，检查 AGENTS.md 全局描述确保无矛盾。Agent 因缺少说明出错时：补充到 .harness/context/agents/，普遍性约束摘录到本文件，更新下方知识库索引。

---

# 二、项目规范（项目相关）

## 仓库结构

```
AGENTS.md              -- AI 知识库入口（本文件）
.harness/
  agents/              -- Agent 角色模板（Orchestrator、Analyst、Coder、Reviewer）
  skills/              -- Skill 定义（迭代功能、构建验证、全局工作流等）
    subskills/         -- Subskill 扫描模板（本项目暂不使用）
  guides/              -- 方法论与参考文档（人工维护）
  context/
    agents/            -- AI 知识库（01-overview ~ 07-key-patterns）
    users/             -- 产品文档（AI只读：01-prd-sense、02-prd-baseline、03-prd-specs）
_config.yml            -- Jekyll 配置文件
_includes/             -- Jekyll 模板片段
_layouts/              -- Jekyll 布局模板
_posts/                -- 已发布的博客文章
_drafts/               -- 草稿文章
images/                -- 博客图片资源
media/                 -- 静态资源（CSS/JS/Fonts）
about/                 -- 关于页面
archives/              -- 归档页面
categories/            -- 分类页面
tags/                  -- 标签页面
drafts/                -- 草稿列表页面
paginator/             -- 分页页面
resource/              -- 其他资源文件
```

## 构建与测试

```bash
# 本地构建
jekyll build

# 本地预览（可选）
jekyll serve
```

## 知识回填规则

知识回填 Phase（迭代功能 Phase 5 / 迭代其它 Phase 5）的回填目标：
- 架构变化 -> 02-architecture.md
- 新术语 -> 04-glossary.md
- 数据结构/存储变化 -> 05-data-boundaries.md
- 新源文件 -> 06-file-map.md
- 新跨文件模式 -> 07-key-patterns.md
- 产品方向调整 -> 提示用户，人工更新 users/01-prd-sense.md 或触发 Skill: 回填产品文档

## 代码生成

以下各节（代码生成、架构边界、质量守护、安全规范）为快速参考摘要，权威定义见 .harness/context/agents/03-conventions.md。

- 使用 Liquid 模板语法，遵循 Jekyll 规范
- Markdown 文章使用 kramdown 解析
- 文章头部必须包含 YAML Front Matter（layout、title、date 等）
- 文件名格式：YYYY-MM-DD-title.markdown 或 YYYY-MM-DD-title.md

## 架构边界

本项目为静态博客站点，架构简单：
- 表现层：HTML 模板（_layouts/、_includes/）
- 内容层：Markdown 文章（_posts/、_drafts/）
- 配置层：Jekyll 配置（_config.yml）
- 资源层：静态文件（images/、media/）

## 质量守护

- 构建验证：执行 `jekyll build` 确保无错误
- 文章格式：符合 Markdown 规范，Front Matter 完整
- 链接检查：确保内部链接有效

## 安全规范

- 不在文章中泄露敏感信息（密钥、密码等）
- 外部链接使用 rel="noopener noreferrer"
- 评论系统（如有）需防范 XSS

## 上下文知识库

| 文件 | 何时查阅 |
|------|---------|
| .harness/context/users/01-prd-sense.md | 功能迭代前，确认产品定位和判断准则 |
| .harness/context/agents/01-overview.md | 任务开始时，了解项目边界 |
| .harness/context/agents/02-architecture.md | 涉及模块新增、跨层调用时 |
| .harness/context/agents/03-conventions.md | 涉及编码/UI/质量/安全约定细节时 |
| .harness/context/agents/04-glossary.md | 对术语不清楚时 |
| .harness/context/agents/05-data-boundaries.md | 涉及数据结构、存储格式时 |
| .harness/context/agents/06-file-map.md | 确定功能对应源文件时 |
| .harness/context/agents/07-key-patterns.md | 实现跨模块模式时 |
| .harness/context/users/02-prd-baseline.md | 确认功能需求与产品约束时 |
| .harness/context/users/03-prd-specs.md | 了解原始需求规格或历史逻辑时 |
| .harness/guides/00-harness-desc.md | 了解 Harness 体系描述时 |
| .harness/guides/01-harness-ops.md | 了解 Harness 运维操作时 |
| .harness/guides/02-harness-dev.md | 了解 Harness 开发流程时 |