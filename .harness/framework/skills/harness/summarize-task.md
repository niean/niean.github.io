---
name: summarize-task
description: 输出任务总结，含变更范围、关键决策和后续建议
---

# Skill: 总结任务

## 步骤

1. 从各 Phase 检查点摘要和 plan 文件（如有）提取任务过程
2. 按报告模板组织总结内容
3. 总结报告在同一条回复中输出并结束任务

## 报告模板

```
## 任务总结

### 需求描述
1. 目标1
2. 目标2

### 关键步骤
Workflow 定义中涉及 2+ 个不同 Agent 角色时标注执行 Agent；仅 Orchestrator 单角色执行时无需标注。
1. 步骤1
2. 步骤2

### 结果验收
- 最终交付物
- 构建/测试

### 合规审计
- 是否遵守 .harness/framework/FRAMEWORK.md 和 .harness/PROJECT.md 约束
- 有无违规或豁免

### 执行统计
- Phase 数量、subagent 调用次数、文件变更数
```
