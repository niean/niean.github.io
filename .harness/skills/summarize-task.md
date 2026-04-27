# Skill: 总结任务

触发：AI 自动触发，按 `Skill: 迭代功能` 或 `Skill: 迭代其它` 流程执行的任务完成后 必须自动执行

本 Skill 采用单 Agent 架构，由主 Agent 直接执行。

## 步骤

1. 回顾任务完整过程
2. 按报告模板输出，通过 `ask_followup_question` 的 question 参数承载完整报告（Cline 环境下纯文本不可见）
3. `[GATE]` 总结报告与 attempt_completion 不得合并；先输出报告 -> 立即结束当前回复 -> 用户确认收到 -> attempt_completion；禁止在同一条回复中调用 `attempt_completion`

## 报告模板

```
## 任务总结

### 意图识别
1. 目标1
2. 目标2

### 关键步骤
多 Agent 架构时标注执行 Agent；单 Agent 无需标注。
1. 步骤1
2. 步骤2

### 结果验收
- 最终交付物
- 构建/测试

### 合规审计
- 是否遵守 AGENTS.md 约束
- 有无违规或豁免

### 资源消耗
- 耗时、Token、工具调用次数
```
