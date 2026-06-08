---
name: scan-harness
description: 扫描 .harness/ 目录下的文档体系，发现不利于AI理解和执行的结构性及语义性问题
---

# Skill: 扫描Harness文档

扫描 `.harness/` 文档体系，发现影响 AI 理解、调度、执行的问题并输出修复建议。

---

## 输入

| 参数 | 必需 | 说明 |
|------|------|------|
| scope | 否 | 扫描范围：`all`（默认，全部维度）、逗号分隔的维度编号（如 `1,2,4`）、或 `structural`（仅1-4）/ `semantic`（仅5-7） |
| level | 否 | 最低报告等级：`all`（默认，E+W+I）、`W`（E+W）、`E`（仅E） |

---

## 问题等级

按对 AI 执行的影响程度分三级：

| 等级 | 含义 | 判定标准 |
|------|------|---------|
| E (Error) | 执行阻断 | AI 无法正确执行或会产生错误结果 |
| W (Warning) | 执行风险 | AI 可执行但可能偏离预期 |
| I (Info) | 改善建议 | AI 可正常执行，有优化空间 |

各维度的默认等级及升降级规则：

| 维度 | 默认 | 升降级条件 |
|------|------|-----------|
| 1 引用完整性 | E | Workflow/Skill/Agent 正文路径断裂 -> E；代码块示例中路径 -> W |
| 2 注册同步性 | W | 已注册但文件不存在 -> E；文件存在未注册 -> W |
| 3 元数据规范 | W | Skill/Workflow 缺 frontmatter -> W；knowledge/prd/lessons 缺 SUMMARY -> I |
| 4 依赖方向 | W | R1(FW->PRJ 反向依赖) -> E；其他规则 -> W |
| 5 跨文件一致性 | E | 规则矛盾 -> E；描述偏差 -> W |
| 6 AI可执行性 | W | 无退出条件/优先级冲突 -> E；模糊量词 -> W |
| 7 上下文效率 | I | 大段重复(>500 tokens) -> W；其他 -> I |
| 8 其他发现 | W | AI 自主判定 |

---

## 扫描维度

### 结构性维度（可自动化检测）

#### 维度1: 引用完整性

检查 `.harness/` 下所有 .md 文件中出现的文件路径和 @引用，验证目标文件是否存在。

检查项：
- 正文中的 `.harness/...` 路径、项目根相对路径
- @引用（`@.harness/...`、`@AGENTS.md` 等）
- 表格中的文件路径列
- 代码块中的路径引用（如构建命令中的项目名）

输出：不存在的路径 + 所在文件及行号

#### 维度2: 注册同步性

检查 FRAMEWORK.md 和 PROJECT.md 中的注册表（Agents/Workflows/Skills/知识索引/扫描维度）与实际文件的双向一致性。

检查项：
- 注册表条目指向的文件是否存在
- 实际存在的 Agent/Workflow/Skill 文件是否已注册
- 知识层级关系图中的路径是否与实际一致
- 目录结构描述与实际目录是否同步

输出：未注册的文件 / 注册但不存在的条目 / 结构描述不一致项

#### 维度3: 元数据规范

检查文件必需的元数据是否齐全。

检查项：
- Skill/Workflow/Agent .md 文件：是否有 YAML frontmatter（name + description）。范围限定为 FRAMEWORK.md 注册表中列出的文件，不含 superpowers/ 子目录内的辅助文件（prompt模板、README等属于外部依赖内部结构）
- `.harness/knowledge/*.md`、`.harness/prd/*.md`、`.harness/lessons/*.md`：首行是否为 `<!-- SUMMARY: ... -->` 格式
- frontmatter 中 name/description 是否为空

输出：缺失元数据的文件列表

#### 维度4: 依赖方向

检查文件间的引用方向是否符合层级约束。层级定义见 00-harness-desc.md 1.3 节和 3.3 节。

层级关系：
```
Layer 0   AGENTS.md -> FRAMEWORK.md(FW) + PROJECT.md(PRJ)
Layer 1   agents/         (角色设定)
Layer 1.5 workflows/      (流程编排)
Layer 2   skills/         (功能单位)
Layer 3   subskills/      (原子操作)
数据层    knowledge/ + prd/ + lessons/ + guides/
```

区分标准 -- 结构依赖 vs 操作性引用：
- 结构依赖（需检查）：文件的规则/逻辑依赖另一文件的内容定义。判断：删除被引用文件后，当前文件的规则/逻辑是否失效
- 操作性引用（跳过）：文件指示 Agent 读取/处理另一文件作为任务操作。如 load-knowledge 读取 knowledge/ 目录

检查项：

跨体系：
- R1: FW -> PRJ 反向依赖：framework/ 下文件引用 PROJECT.md 以外的项目文件（如knowledge/、prd/、lessons/project.md、specs/、plans/）

能力层垂直方向：
- R2: Skill -> Workflow：Skill 文件引用 Workflow 文件路径或 Phase 编号
- R3: Skill -> Agent：Skill 文件引用 Agent 文件路径或声明由哪个 Agent 执行
- R4: Agent -> Workflow Phase：Agent 文件引用 Workflow 的 Phase 编号或流程细节
- R5: Subskill -> 上层：Subskill 文件引用 Skill/Agent/Workflow 的具体定义

能力层水平方向：
- R6: Workflow -> Workflow：Workflow 之间互相引用（各自独立编排）
- R7: Agent -> Agent：Agent 之间互相引用

数据层：
- R8: 数据层 -> 能力层：knowledge/、prd/、lessons/ 引用 agents/、workflows/、skills/ 的具体定义

声明性约束：
- R9: Skill description 包含触发时机（如"Phase X 时调用""当...时触发"），description 只描述功能用途
- R10: Agent 文件定义执行步骤编排（Step 序列、Phase 流程），Agent 只定义角色和能力边界

允许的例外：
- FRAMEWORK.md 引用 PROJECT.md（FW/PRJ 桥接接口）
- PROJECT.md <-> knowledge/03-conventions.md 双向声明（摘要-权威源关系）
- knowledge/01-overview.md 指回 AGENTS.md（入口指引）
- Skill 对数据层文件的操作性引用（如 load-knowledge 读取 knowledge/ 目录）
- Agent 声明 Skill 分类（如 `harness/*`）或 Skill 名称列表（能力声明，非反向引用内部实现）

输出：违规引用（规则编号 + 源文件及行号 + 被引用目标 + 违规说明）

### 语义性维度（需AI理解力判断）

#### 维度5: 跨文件一致性

逐对比对存在引用或摘要关系的文件，发现矛盾。

检查项：
- PROJECT.md "项目规范"摘要 vs knowledge/03-conventions.md 权威源：是否存在规则偏差
- 同一术语在不同文件中定义是否一致（对照 knowledge/21-glossary.md）
- Workflow/Skill 中引用的规则与 FRAMEWORK.md/PROJECT.md 中声明是否一致
- 知识索引表中"何时查阅"描述与文件实际内容是否匹配

输出：矛盾对（文件A vs 文件B） + 具体冲突内容 + 建议以哪个为准

#### 维度6: AI可执行性

逐段审查指令性文本，发现 AI 难以确定性执行的表述。

检查项：
- 模糊量词无量化基准（"适当""合理""少量"等，缺乏具体阈值或示例）
- 条件分支缺退出条件（"如果...则..."但未说明"否则"路径）
- 隐式前提依赖（步骤假设了未声明的上下文，如"读取上一步的结果"但未明确上一步产出格式）
- 优先级冲突无仲裁规则（多条规则可能同时适用，但未说明哪个优先）
- 循环指令无终止条件（"重复直到满意"等无法判定的条件）

输出：问题文本原文 + 所在文件及位置 + 问题类型 + 改写建议

#### 维度7: 上下文效率

评估文档对 context window 的占用效率。

检查项：
- 跨文件重复：相同或高度相似的段落出现在多个文件中（摘要引用除外）
- 冗余过渡：无信息增量的连接语、重复声明
- 可压缩段落：连续 5+ 行纯叙述段落且内容可结构化为表格/列表时，标记为可压缩
- 死信息：已被其他文件完全覆盖但仍保留的内容

输出：冗余内容位置 + 预估可节省的 token 数（取百位整数，如 ~200 tokens） + 压缩建议

### AI自主扩展

上述7个维度为基线检查项。扫描过程中，AI 如发现以下类型的问题时归入维度8：(1) 同一指令在不同文件中有矛盾表述但不属于维度5的引用关系，(2) 文件编码/格式异常导致无法正确解析，应归入"维度8: 其他发现"一并报告，并建议是否值得固化为新维度。

---

## 执行

### Step 1 -- 确定范围

- 解析 scope 参数，确定本次扫描的维度列表
- 解析 level 参数，确定最低报告等级（默认 all）
- 列出 `.harness/` 下所有 .md 文件（`Glob .harness/**/*.md`），加上根目录的 AGENTS.md、CLAUDE.md
- 排查目录须包含：`.harness/plans/`、`.harness/specs/`
- 输出待扫描文件数、维度列表和报告等级

### Step 2 -- 结构性扫描（维度1-4）

按维度顺序执行，每个维度独立输出结果。可通过 subagent 并行（每维度一个 subagent），无 subagent 能力时主 Agent 顺序执行。

每个维度的 subagent 提示须包含：维度定义、检查项列表、待扫描文件列表、输出格式要求。维度4（依赖方向）的 subagent 还须包含层级定义、R1-R10 规则、允许的例外列表和区分标准。

### Step 3 -- 语义性扫描（维度5-7）

按维度顺序执行。语义性扫描需要跨文件理解，建议：
- 维度5（跨文件一致性）：先读取所有文件的 SUMMARY 建立索引，再按引用关系逐对比对
- 维度6（AI可执行性）：逐文件扫描指令性段落
- 维度7（上下文效率）：在前述维度已读取内容的基础上评估

可通过 subagent 并行，但每个 subagent 需要的上下文较大，建议维度数 <= 3 时不分批。

### Step 4 -- 汇总报告 `[CONFIRM]`

合并所有维度结果，按"问题等级"章节的升降级规则标注每条问题的等级，过滤低于 level 参数的条目，按以下格式输出：

```
# Harness 文档扫描报告

扫描范围：{维度列表}
报告等级：{level}
扫描文件数：N
问题总数：M（E: x / W: y / I: z）

## 维度1: 引用完整性（X项）
| # | 等级 | 文件 | 行号 | 失效引用 | 建议修复 |
|---|------|------|------|---------|---------|

## 维度2: ...（同上格式，各维度表头按维度定义调整，均含等级列）

## 维度8: 其他发现（如有）
| # | 等级 | 文件 | 问题描述 | 建议 | 是否建议固化为新维度 |
|---|------|------|---------|------|-------------------|

## 统计
| 维度 | 问题数 | E | W | I |
|------|--------|---|---|---|
```

结束当前回复，等待用户确认修复范围。

### Step 5 -- 执行修复

按用户确认的范围修复。约束：
- AI-READONLY 文件（agents/、prd/、guides/）：输出修改 Diff，经用户确认后执行
- 其他文件：直接修复
- 修复后检查是否引入新的引用断裂（维度1回归）

### Step 6 -- 输出变更摘要

报告：扫描维度数、问题总数、修复数、跳过数、AI-READONLY 待处理数。
