# Harness Engineering 风格规范

本文档定义了一套项目无关的 AI 协作工程方法论，用于规范 AI Agent 在软件项目中的行为模式。任何项目均可参照本规范搭建自己的 AI 知识库与操作体系。

## 约束

本文仅供自然人使用，未经人工确认、禁止AI修改。

---

## 1. 核心理念

- AI Agent 是受约束的协作者，不是自由发挥的生成器
- 所有 AI 行为由显式规则驱动，规则集中管理、按需加载
- 人工定义的信息与 AI 维护的知识分离存储，权责清晰
- 知识库是活文档，随项目演进持续更新，不允许腐化

---

## 2. 文件体系

### 2.1 入口文件：AGENTS.md

项目根目录的 AGENTS.md 是 AI Agent 的唯一入口：声明项目背景、定义通用/项目规范、索引知识库、注册能力表。AGENTS.md 是索引和规则的聚合点，具体知识分散在各文档中。

### 2.2 统一目录：.harness/

所有 AI 协作基础设施统一放在 `.harness/` 目录下（dot 前缀，类似 .github/ 风格），与应用代码分离。

```
AGENTS.md                  -- 入口文件（项目根目录）
.harness/
  agents/                  -- Agent 角色模板
  skills/                  -- Skill 流程定义
    subskills/             -- Subskill 任务模板
  context/
    agents/                -- AI 知识库（AI 可读写）
    users/                 -- 产品文档（AI 只读）
  guides/                  -- 方法论与参考文档（人工维护）
```

每类知识有且只有一个归属文档，不重复维护。

---

## 3. 能力模型

### 3.1 内容层级

| 层级 | 概念 | 定义 | 目录 | 结构特征 |
|------|------|------|------|---------|
| Layer 1 | Agent | 角色定义 -- "谁来做" | .harness/agents/ | 角色人格、行为规则、决策逻辑、上下文管理 |
| Layer 2 | Skill | 流程编排 -- "怎么做" | .harness/skills/ | 多 Phase 工作流、Agent 分工、门禁决策、检查点交接 |
| Layer 3 | Subskill | 原子任务 -- "做什么" | .harness/skills/subskills/ | 单 Phase 线性流程、输入-规则-输出、无决策 |

Subskill 本质是 Task（原子任务），因 "Task" 在用户对话、IDE 会话等多处已有含义，为避免歧义使用 Subskill 隔离命名空间。

### 3.2 执行机制：subagent

subagent 是通过 `use_subagents` 启动的独立上下文窗口，是运行方式而非内容类型。Agent 和 Subskill 均可通过 subagent 机制运行。两者执行方式相同（独立上下文），但内容定义不同：Agent 有角色和决策能力，Subskill 只有检查规则和输出格式。

### 3.3 层级间关系

- Skill 编排 Agent：每个 Phase 指定执行 Agent
- Skill/Agent 调用 Subskill：通过 subagent 机制并行启动
- Subskill 不反向引用 Skill 或 Agent

---

## 4. Skills

Skill 是可复用的 AI 操作单元：名称 kebab-case，触发方式（人工/自动/调用），有序步骤，结构化输出。所有 Skill 必须在 AGENTS.md 注册。

文件格式：

```markdown
# Skill: {名称}

触发：{触发条件}

步骤：
1. {步骤1}
2. {步骤2}
...
```

---

## 5. 知识库管理

- 按需加载：只读取任务相关文档，不全量加载
- 单一归属：每条知识只在一个文档维护，重复则合并
- 知识回填：代码变更后同步回填到 context/agents/ 对应文档
- 自愈维护：AI 因缺少说明出错时，补充到知识库并同步 AGENTS.md

---

## 6. 规范分层

AGENTS.md 中的规范分两层：

- 通用规范（项目无关）：能力模型、文件管理、知识库管理、自愈维护，可跨项目复用
- 项目规范（项目相关）：仓库结构、构建命令、编码约定、架构边界、质量守护、安全规范，按项目定制

---

## 7. 人机协作边界

| 角色 | 职责 | 权限 |
|------|------|------|
| 人工 | 定义需求、确认方案、审批删除 | 读写 context/users/ 和 guides/，审批 AI 变更 |
| AI | 按规则执行、维护知识库、输出摘要 | 读写 context/agents/，只读 context/users/ |

- AI 遇模糊需求必须询问，不自行决定产品方向
- 删除操作必须人工确认
- users/ 与 agents/ 冲突时以 users/ 为准

---

## 8. 新项目接入

1. 创建 AGENTS.md（项目背景 + 通用规范 + 项目规范）
2. 创建 .harness/context/agents/（架构、约定、术语等知识库）
3. 创建 .harness/context/users/（产品需求等人工文档）
4. 创建 .harness/skills/（可复用操作定义）
5. 在 AGENTS.md 注册能力表和知识库索引
