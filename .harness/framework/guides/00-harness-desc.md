# Harness Engineering 风格规范

本文档定义了一套项目无关的 AI 协作工程方法论，用于规范 AI Agent 在软件项目中的行为模式。任何项目均可参照本规范搭建自己的 AI 知识库与操作体系。

## 约束

本文仅供自然人使用，未经人工确认、禁止AI修改；允许AI蒸馏，但输出必须沿用原文、不得修改内容。

---

## 1.核心理念

## 1.1 指导思想

- AI Agent 是受约束的协作者，不是自由发挥的生成器
- 所有 AI 行为由显式规则驱动，规则集中管理、按需加载
- 人工定义的信息与 AI 维护的知识分离存储，权责清晰
- 知识库是活文档，随项目演进持续更新，不允许腐化


### 1.2 分层建设

Harness 只做顶层调度 -- 知识孪生、CI/CD等流程编排；实施层尽量复用优秀的开源工具（如 superpowers、BMAD），不自建。

```
+---------------------------------------------------------------+
|                    Harness（顶层调度）                          |
|  知识孪生 (.harness/knowledge/)                                |
|  流程编排 (AGENTS.md, framework/skills/, framework/agents/)    |
|  CI/CD (尚未实现)                                              |
+---------------------------------------------------------------+
        |                       |                       |
        v                       v                       v
+----------------+   +------------------+   +------------------+
| superpowers    |   | BMAD             |   | 其它开源工具       |
| 开发方法论技能   |   | 需求/设计方法论     |   | 按需引入          |
+----------------+   +------------------+   +------------------+
        |                       |                       |
        v                       v                       v
+---------------------------------------------------------------+
|                 AI Agent 运行时（底层执行）                      |
|  Claude Code / Gemini CLI / 其它 Agent 平台                    |
+---------------------------------------------------------------+
```

- 顶层（Harness）：定义知识、规则和流程，决定"做什么"和"谁来做"
- 实施层（开源工具）：提供方法论和具体执行策略，决定"怎么做"
- 底层（AI Agent 运行时）：提供工具调用、文件操作、代码生成等基础能力

### 1.3 任务调度

任务调度遵循如下的四层架构，引用关系自上而下、禁止反向、禁止跨层

```
Orchestrator：任务调度，顶层调度、任务分类
   ↓ 
   Workflow：流程编排，每个Phase由Agent+Skill构成
        ↓ 
        Agent：角色设定，治理单位，控制Skill列表、LLM列表、权限列表等（不实现具体功能）
        Skill：功能单位，内部可编排多个 Subskill，对外呈现单一功能
             ↓ 
             Subskill：原子操作，不可再拆、只做底层动作

备注：任务调度中，没有Subagent、Role、Command等实体概念。特别的，Subagent是一种技术手段，不是子Agent。

```


---

## 2. 文件体系

### 2.1 入口文件

项目根目录的 AGENTS.md 是 AI Agent 的平台路由入口，通过 `@` 指令加载 `.harness/framework/FRAMEWORK.md`（通用规范、注册表）和 `.harness/PROJECT.md`（项目配置、规则摘要）。具体知识分散在各文档中。

### 2.2 统一目录：.harness/

所有 AI 协作基础设施统一放在 `.harness/` 目录下（dot 前缀，类似 .github/ 风格），与应用代码分离。完整目录结构见 PROJECT.md "仓库结构"。每类知识有且只有一个归属文档，不重复维护。

---

## 3. 能力模型

### 3.1 内容层级

| 概念 | 定义 | 目录 | 结构特征 |
|------|------|------|---------|
| Agent | 角色与能力 -- "谁来做、能做什么" | .harness/framework/agents/ | 角色、能力(原子项)、约束、上下文管理 |
| Workflow | 流程编排 -- "按什么顺序做" | .harness/framework/workflows/ | 多 Phase 工作流、Agent 分工、门禁决策、检查点交接 |
| Skill | 功能单位 -- "怎么做" | .harness/framework/skills/ | 输入-步骤(Step)-输出，可编排多个 Subskill，对外呈现单一功能 |
| Subskill | 原子任务 -- "做什么" | .harness/framework/skills/harness/subskills/ | 单步线性流程、输入-规则-输出、无决策 |

Workflow 本质是端到端编排（如迭代功能、修复Bug、迭代文档），拆分自早期的"大 Skill"概念。与 Skill 的区别：Workflow 有 Phase、GATE 门禁和 Agent 分工；Skill 有 Step、无门禁、由上层指定执行 Agent。

Subskill 本质是 Task（原子任务），因 "Task" 在用户对话、IDE 会话等多处已有含义，为避免歧义使用 Subskill 隔离命名空间。

阶段命名规范：Workflow 的阶段称为 Phase，Skill 的阶段称为 Step，其它场景使用 Todo。Harness 引用外部依赖时，阶段简化为英文首字母：Phase -> P、Step -> S、Task/Todo -> T。

### 3.2 执行机制：subagent

subagent 是通过 Agent 工具启动的独立上下文窗口，是运行方式而非内容类型。Agent 和 Subskill 均可通过 subagent 机制运行。两者执行方式相同（独立上下文），但内容定义不同：Agent 有角色和决策能力，Subskill 只有检查规则和输出格式。

### 3.3 层级间关系与引用方向

- Skill 不声明自身由哪个 Agent 执行，执行角色由上层指定
- Skill 不声明自身的触发时机，调用时机由上层（Workflow/Orchestrator）决定；Skill 的 description 只描述功能用途
- Skill/Agent 调用 Subskill：通过 subagent 机制并行启动
- Agent 不反向引用 Skill（如具体 Phase 编号、Skill 文件名），不定义执行流程
- Subskill 不反向引用 Skill 或 Agent
- 引用方向自上而下：上层引用下层，同层可编排引用，下层仅允许"指回入口"式引用
- 允许的特例：PROJECT.md 与 03-conventions.md 双向声明摘要-权威源关系；01-overview.md 指回 FRAMEWORK.md 或 PROJECT.md

---

### 3.5 Workflows

Workflow 是端到端编排，通过多个 Phase 协调多个 Agent 角色完成复杂任务。注册表和执行规则（GATE 门禁、检查点交接、上下文管理）见 FRAMEWORK.md。

---

## 4. Skills

Skill 是可复用的功能单位，通过有序 Step 完成特定任务。项目自维护 Skill 必须在 `.harness/framework/FRAMEWORK.md` 注册；外部依赖能力（如 superpowers 插件）由平台提供，在 `.harness/framework/FRAMEWORK.md` 单独声明来源，不逐一注册。

### 4.1 核心要素

Skill 由 Workflow Phase、其它 Skill 或人工指令调用，按有序 Step 执行。执行约束见 FRAMEWORK.md。

### 4.2 设计原则

参照 Anthropic Skill 最佳实践与 Harness 工程约束：

- 简洁优先：Skill 文件是流程骨架，不是教程；AI 已具备通用能力，只补充它不知道的上下文
- 自由度分级：流程关键路径（构建、安全扫描）用低自由度（精确命令）；探索性任务（需求设计）用高自由度（启发式指引）
- 渐进加载：Skill 主文件作为目录，详细内容拆分到子文件（superpowers/、subskills/），按需读取
- 反馈闭环：扫描 -> 修复 -> 验证的循环结构，确保问题不遗漏

### 4.3 文件格式

Skill 主文件（`.harness/framework/skills/` 下）：

```markdown
---
name: skill-name
description: 一句话描述 Skill 功能用途（不含触发时机）
---

# Skill: {显示名}

## 输入

| 参数 | 必需 | 说明 |
|------|------|------|
| {param} | {是/否} | {说明} |

## 步骤

### Step 1 -- {步骤名}
{具体步骤}

### Step 2 -- {步骤名}
{具体步骤}

## 输出
{输出格式或模板}
```

可选节（按需添加，不作为默认结构）：
- `## 上下文管理`：Skill 有特殊加载策略时添加
- `检查点`：多 Phase Workflow 中 Agent 交接时添加

### 4.4 Subskill

Subskill 是原子任务模板（无 Phase 编排、无决策），由 Skill 或 Agent 通过 subagent 机制调度。详见 3.1 内容层级。

文件格式（`.harness/framework/skills/harness/subskills/` 下）：

```markdown
# Subskill: {显示名}

## 任务
{一句话描述}

## 输入
- {files}：文件路径列表

## 检查规则
{逐条列出}

## 输出格式
{结构化表格模板}
```

---

## 5. 其他规范

- 知识库管理：按需加载、单一归属、知识回填、自愈维护，详见 FRAMEWORK.md
- 规范分层：通用规范在 FRAMEWORK.md，项目规范在 PROJECT.md
- 人机协作：AI 遇模糊需求必须询问；删除必须人工确认；prd/ 优先于 knowledge/，详见 FRAMEWORK.md
- 新项目接入：见 02-harness-dev.md "项目初始化"
