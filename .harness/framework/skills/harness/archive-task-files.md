---
name: archive-task-files
description: 归档当前 Task 的 spec 和 plan 文件，从 active/ 移到 completed/，不影响其他 Task 的活跃文件
---

# Skill: 归档任务文件

## 输入

| 参数 | 必需 | 说明 |
|------|------|------|
| spec_file | 否 | spec 文件路径（如 `.harness/specs/active/spec-260331-xxx.md`）；未提供则跳过 spec 归档 |
| plan_file | 否 | plan 文件路径（如 `.harness/plans/active/plan-260331-xxx.md`）；未提供则跳过 plan 归档 |

两个参数均未提供时，输出"无需归档"并结束。

## 步骤

### Step 1 -- 校验源文件

对每个输入文件，校验文件存在于 `.harness/specs/active/` 或 `.harness/plans/active/`。文件不存在时报错并跳过该文件。

### Step 2 -- 更新文件状态

对每个输入文件，将文件内的状态字段更新为 `completed`（如有）。

### Step 3 -- 更新内部引用

归档前，检查 spec 和 plan 文件之间的相互引用路径：
- plan 引用 spec 时：将 `.harness/specs/active/` 更新为 `.harness/specs/completed/`
- spec 引用 plan 时：将 `.harness/plans/active/` 更新为 `.harness/plans/completed/`

仅更新本次归档涉及的文件内部引用，不修改其他文件。

### Step 4 -- 移动文件

执行归档移动：
- `.harness/specs/active/{file}` -> `.harness/specs/completed/{file}`
- `.harness/plans/active/{file}` -> `.harness/plans/completed/{file}`

使用 `git mv` 移动（文件已在版本控制中时），否则使用 `mv`。

### Step 5 -- 归档后校验

对每个已移动的文件，校验以下内容：
- 状态字段值为 `completed`（非 `active`）
- 文件内不包含 `specs/active/` 或 `plans/active/` 路径引用
- 文件内不包含已废弃路径（如 `superpowers-ref/`）

校验不通过时，就地修复后继续。

### Step 6 -- 输出归档摘要

输出格式：

```
归档完成：
- spec: {文件名} -> .harness/specs/completed/
- plan: {文件名} -> .harness/plans/completed/
```

未归档的文件类型省略对应行。
