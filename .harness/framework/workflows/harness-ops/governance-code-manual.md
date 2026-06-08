---
name: governance-code-manual
description: 人工指令触发代码治理
---

# Workflow: 治理代码-人工

---

## Phase 1: 调度
- Agent: Orchestrator
- 读取 .harness/PROJECT.md "项目规范"（代码生成、架构边界、质量守护、安全规范），启动 Phase 2

## Phase 2: 扫描
- Agent: Reviewer（subagent 并行）；可传入 model 参数指定扫描 subagent 使用的 LLM 模型
- 读取 .harness/PROJECT.md "扫描维度" 表，使用 `.harness/framework/skills/harness/subskills/scan-dimension.md` 通用模板，通过 Agent 工具并行启动扫描（传入 dimension 和 rule_sources）。（降级见 FRAMEWORK.md）
- 维度数量超 5 个时分 2 批执行（每批不超过 5 个），批间无需等待用户确认
- 每个维度必须有独立扫描结论，禁止跳过或虚报

检查点：`[Phase 2 扫描] N个维度完成, 共M项违规 (安全X, 架构Y, ...)`

## Phase 3: 汇总与确认 `[GATE]`
- Agent: Orchestrator
- 合并结果，按严重程度排序（安全 > 架构 > 图片 > 日志 > 编码 > 废弃代码）
- 向用户展示违规清单，结束当前回复，等待确认

## Phase 4: 修复 `[GATE-ENTRY]`
- Agent: Coder
- `[GATE-ENTRY]` 前置条件：用户已在上一条消息中明确确认违规清单
- 按确认清单修复，遵守 coder.md 约束（TDD 适用范围由 coder.md 定义）和 .harness/PROJECT.md 代码生成规范
- 同步更新 .harness/knowledge/22-file-map.md（如有文件删除）

检查点：`[Phase 4 修复] 修复N项, 删除M个废弃项, 更新file-map: 是/否`

## Phase 5: 验证
- Agent: Reviewer；沿用 Phase 2 传入的 model 参数

### Step 5a: 构建验证（主 Agent）
执行 `Skill: 结果验收`（`.harness/framework/skills/harness/verify-acceptance.md`），scope=build_only，确认零警告零错误。失败回 Phase 4（Phase 4 -> Phase 5 循环最多执行 3 轮，含首次，超限时中断流程输出错误报告）。

### Step 5b: 回归扫描（可选，修复涉及 3+ 个文件或跨越 2+ 个扫描维度时）
对修复涉及的文件重新执行 Phase 2 中相关维度的扫描，确认无新增违规或残留问题。（降级见 FRAMEWORK.md）。发现新增违规或残留问题时回到 Phase 4 修复后重新执行 Step 5a+5b，Phase 4 -> Phase 5 循环最多执行 3 轮（含首次），超限时中断流程输出错误报告。

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
