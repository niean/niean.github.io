# Skill: 治理代码

触发：人工指令。对项目代码进行完整质量治理。

本 Skill 采用多 Agent 编排，每个 Phase 指定执行角色。Phase 间通过"检查点摘要"（不超过 10 行）交接上下文。

---

## Phase 1: 调度
- Agent: Orchestrator
- 读取 AGENTS.md 中的代码生成、质量守护、安全规范，启动 Phase 2

## Phase 2: 扫描
- Agent: Reviewer（subagent 并行）
- 通过 `use_subagents` 启动扫描，读取 `.harness/skills/subskills/` 对应模板作为 prompt。无 subagent 能力时主 Agent 顺序执行
- 本项目暂不配置 Subskills，扫描基于 AGENTS.md 和 03-conventions.md 中的质量守护、安全规范、架构边界规则执行
- 每个维度必须有独立扫描结论，禁止跳过或虚报

检查点：`[Phase 2 扫描] N个维度完成, 共M项违规 (安全X, 架构Y, ...)`

## Phase 3: 汇总与确认
- Agent: Orchestrator
- 合并结果，按严重程度排序（安全 > 架构 > 其它）
- 通过 ask_followup_question 向用户展示违规清单，等待确认

## Phase 4: 修复
- Agent: Coder
- 读取 `.harness/agents/coder.md`，按确认清单修复
- 同步更新 06-file-map.md（如有文件删除）

检查点：`[Phase 4 修复] 修复N项, 删除M个废弃项, 更新file-map: 是/否`

## Phase 5: 验证
- Agent: Reviewer

### Step 5a: 构建验证（主 Agent）
```bash
jekyll build
```
零警告。失败回 Phase 4。

### Step 5b: 回归扫描（可选，修复涉及面广时）
对修复涉及的文件重新执行 Phase 2 中相关维度的扫描，确认无新增违规或残留问题。无 subagent 时主 Agent 顺序执行。

检查点：`[Phase 5 验证] 构建: 通过/失败, 回归扫描: 通过/跳过/N项残留`

## Phase 6: 收尾
- Agent: Orchestrator
- 输出治理报告：扫描维度数、违规数、修复数、剩余数

---

## 上下文管理

1. Phase 2 扫描 subagent 各有独立上下文
2. Phase 3 只需汇总文本，不加载源码
3. Phase 4 只加载修复文件，不加载全部扫描文件
4. 所有 Phase 均为必选项，禁止因上下文压力跳过
