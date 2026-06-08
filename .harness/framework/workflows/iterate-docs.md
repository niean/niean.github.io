---
name: iterate-docs
description: 文档迭代端到端工作流，单 Agent 完成从知识加载到一致性验证的全流程
---

# Workflow: 迭代文档

5 阶段单 Agent 编排：harness（知识库加载）-> 直接操作（变更方案 -> 执行变更 -> 一致性验证 -> 变更报告）。

核心价值：修改目标文件后，自动检查整个文档体系，同步修改其它文件中的引用、依赖、相似描述，防止文档体系碎片化。

---

## 进度清单

执行时复制此清单追踪进度：

```
Workflow Progress:
- [ ] Phase 1: 知识加载（知识库加载、约束确认）
- [ ] Phase 2: 变更方案（识别目标、扫描受影响文件）[GATE]
- [ ] Phase 3: 执行变更（按方案修改目标和受影响文件）[GATE-ENTRY]
- [ ] Phase 4: 一致性验证（全量扫描、交叉验证）
- [ ] Phase 5: 变更报告
```

---

## Phase 1: 知识加载
- Agent: Orchestrator
- 执行 `Skill: 加载知识库`（`.harness/framework/skills/harness/load-knowledge.md`），参数 task_type=docs, is_first_load=true
- 确认约束与文档体系结构

检查点：`[Phase 1 知识加载] 索引: N个文件, 必读: 已加载M个, 按需: K个可查阅`

## Phase 2: 变更方案 `[GATE]`
- Agent: Orchestrator
- 识别用户要修改的目标文件和修改意图
- 检查目标文件是否标记为 AI-READONLY；若是，提示用户确认后才能继续
- 读取目标文件完整内容，理解当前描述
- 根据修改意图，拟定具体变更内容
- 扫描文档体系，识别所有受影响的文件：
  - 必须执行：grep 搜索目标文件路径、目标实体名称（含变更前后的名称）在 `.harness/` 全部 .md 文件和AGENTS.md、.harness/framework/FRAMEWORK.md、.harness/PROJECT.md 中的所有引用；禁止仅凭记忆枚举受影响文件，必须以 grep 结果为准
  - 引用关系：其它文件中引用了目标文件的内容（如 .harness/PROJECT.md 摘要引用 knowledge/ 权威源）
  - 依赖关系：其它文件的逻辑依赖目标文件的定义（如 Skill 文件引用 Agent 角色名称）
  - 相似描述：其它文件中有与目标文件相同或相似的描述（如同一规则在多处出现）
  - 索引关系：目标文件在 .harness/framework/FRAMEWORK.md 注册表、.harness/PROJECT.md 知识索引中的注册信息
- 向用户输出变更方案摘要：

```
目标文件: {文件路径}
变更内容: {具体修改项}
受影响文件:
  - {文件路径}: {影响类型(引用/依赖/相似/索引)} - {需同步的内容}
  - ...
```

- `[GATE]` 规则见 FRAMEWORK.md

检查点：`[Phase 2 变更方案] 目标: N个文件, 受影响: M个文件, 状态: 已确认`

## Phase 3: 执行变更 `[GATE-ENTRY]`
- Agent: Orchestrator
- `[GATE-ENTRY]` 前置条件：用户已在上一条消息中明确确认变更方案
- 按确认方案执行修改，顺序：
  1. 修改目标文件
  2. 同步受影响文件（按依赖顺序：权威源 -> 摘要引用 -> 索引注册）
  3. AI-READONLY 文件的同步修改需逐个提示用户确认
- 每个文件修改后立即验证：确认修改内容与方案一致，无遗漏

检查点：`[Phase 3 执行变更] 修改: N个文件, 同步: M个文件`

## Phase 4: 一致性验证
- Agent: Orchestrator
- 全量扫描文档体系，验证一致性：
  - 必须执行：grep 搜索所有已变更的实体名称和文件路径在 `.harness/` 全部 .md 文件和AGENTS.md、.harness/framework/FRAMEWORK.md、.harness/PROJECT.md 中的引用，确认全部已同步；禁止仅凭 Phase 2 方案验证，必须以 grep 结果为准
  - 交叉引用完整性：所有引用指向有效文件和章节
  - 术语一致性：同一概念在各文件中使用相同术语
  - 索引同步：.harness/framework/FRAMEWORK.md 中的 Workflows/Skills/Agents 注册表、.harness/PROJECT.md 中的知识索引与实际文件一致
  - 命名规范：文件名 kebab-case、Skill 显示名中文、Agent 名称英文
  - 引用方向：下层不反向引用上层具体定义（特例见 .harness/framework/guides/00-harness-desc.md 3.3 节）
- 发现不一致时：非 AI-READONLY 文件自动修复（以权威源为准）；内容冲突且无法确定权威源时，记录到变更报告并提示用户决策
- AI-READONLY 文件的修复需提示用户确认

检查点：`[Phase 4 一致性验证] 扫描: N个文件, 不一致: M项, 修复: K项`

## Phase 5: 变更报告
- Agent: Orchestrator
报告内容：
- 目标文件变更摘要
- 同步修改的文件列表及具体变更
- 一致性验证结果（通过/修复项）
- AI-READONLY 文件是否涉及（已确认/未涉及）

---

## 上下文管理

1. Phase 1 通过 Skill: 加载知识库 加载文档索引，不加载全部文件内容
2. Phase 2 按需读取目标文件和可能受影响的文件
3. Phase 3 逐文件修改，不批量加载
4. Phase 4 逐文件扫描验证
