---
name: verify-acceptance
description: 对变更代码执行构建验证、规范扫描和验收检查
---

# Skill: 结果验收

## 输入参数

| 参数 | 必需 | 说明 |
|------|------|------|
| scope | 否 | 执行范围：`full`（默认，构建+扫描+验收）、`build_only`（仅构建，用于代码治理等场景） |
| changed_files | scope=full 时必需 | 本次变更文件列表 |
| spec_criteria | scope=full 时必需 | 验收标准（由调用方提供，如 spec.test_criteria、回归验证条件） |
| spec_reviewed | 否 | 布尔，默认 false；调用方已通过 subagent spec review 时设为 true |

## 约束

- 扫描范围：仅本次变更文件
- 每个 Step 必须实际执行并产出独立结果，禁止跳过或虚报
- 不通过时返回调用方修复（反馈环路）

## 步骤

```
Task Progress:
- [ ] Step 1: 构建验证
- [ ] Step 2: 代码扫描（scope=full）
- [ ] Step 3: 验收检查（scope=full）
```

### Step 1: 构建验证

构建：执行 .harness/PROJECT.md "构建与测试" 中定义的构建命令，确认零警告零错误。

测试：测试命令同样取自 .harness/PROJECT.md "构建与测试"。

scope=build_only 时，Step 1 完成后输出结果摘要并结束。

### Step 2: 代码扫描

读取 .harness/PROJECT.md "扫描维度" 表，使用 `.harness/framework/skills/harness/subskills/scan-dimension.md` 通用模板，根据变更文件类型匹配维度（文件类型与维度的映射见 .harness/PROJECT.md "扫描维度"表）；涉及文件删除 -> 追加废弃代码维度。subagent 并行扫描（传入 dimension 和 rule_sources），每个维度独立输出结论。超 5 个维度时分 2 批执行（每批不超过 5 个），批间无需等待。

### Step 3: 验收检查

对照 spec_criteria 逐项验证，输出每项通过/不通过。

通过检查点摘要中包含 'spec_reviewed: true' 标记判断调用方是否已通过 subagent spec review。如果 spec_reviewed 为 true（如 subagent-driven-development 的 spec compliance reviewer），可跳过逐项 spec 合规检查，仅验证：(1) 全部 Blocking 级验收标准，(2) 跨 task 集成点。

## 严重程度分级

| 级别 | 判断标准 | 处理方式 |
|------|---------|---------|
| Blocking | 安全漏洞、构建失败、架构边界违规、验收标准不通过 | 必须修复后重新验收 |
| Warning | 编码约定偏离、可优化的处理逻辑、日志格式不规范 | 本次任务中修复 |
| Info | 废弃代码、可选优化、非本次引入的既存问题 | 记录到 .harness/plans/debt-tracker.md |

- 新发现的既存问题（非本次引入）记录到技术债跟踪文件 `.harness/plans/debt-tracker.md`，不强制在本次迭代修复
- 本次任务新引入的技术债，必须修复、修复后重新扫描验证

## 输出

通过：
```
[结果验收] 构建: 通过, 扫描: N维度/0违规, 验收标准: M项通过
```

不通过时输出违规清单（级别/build_issues/scan_issues/criteria_check），Blocking 和 Warning 交回修复后重新验收，Info 记录技术债。

scope=build_only 时：
```
[结果验收] 构建: 通过/失败
```
