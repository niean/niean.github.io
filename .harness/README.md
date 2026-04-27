# Harness 工程模板

本目录包含项目无关的 Harness 工程模板，供新项目快速接入 AI 协作工程体系。所有 `{{占位符}}` 需根据项目实际情况替换。

## 约束

本模板系通过 `claude-opus-4.6`模型调教，可能使用了专有的函数、方法等，如遇问题请自行修正

## 项目初始化

请参考 `guides/02-harness-dev.md`中的 `## 项目初始化`章节

## 开发流程

请参考 `guides/02-harness-dev.md`中的 `## 人机协作开发`章节

## 知识库层级关系
```
Layer 0  AGENTS.md（顶层入口、注册表、规则摘要）
            |
            |-- 注册 --> agents/、skills/（含 subskills/）全部文件
            |-- 索引 --> context/agents/、context/users/、guides/ 全部文件
            |-- 摘要引用 --> context/agents/03-conventions.md（权威源）
            |
Layer 1  .harness/agents/（Agent 角色定义 -- "谁来做"）
            |
            |-- orchestrator.md  读取 AGENTS.md，引用 iterate-feature.md、reviewer.md
            |-- analyst.md       读取 AGENTS.md，读取 context/users/、context/agents/
            |-- coder.md         读取 AGENTS.md，按需读取 context/agents/03、07
            |-- reviewer.md      引用 skills/subskills/scan-*.md（调度扫描）
            |
Layer 2  .harness/skills/（Skill 流程定义 -- "怎么做"）
            |
            |-- iterate-feature.md    引用 agents/analyst.md、coder.md、reviewer.md
            |-- iterate-other.md
            |-- governance-code.md    引用 agents/coder.md、reviewer.md，调度 skills/subskills/
            |-- governance-capability.md  读取 AGENTS.md 注册表 + agents/、skills/（含 subskills/）
            |-- governance-all.md     编排 governance-code、governance-capability、backfill-knowledge、backfill-prd
            |-- backfill-knowledge.md 读取 AGENTS.md、context/agents/、skills/目录（含 subskills/）
            |-- backfill-prd.md       读取 context/users/ 三个产品文档
            |-- verify-build.md       独立（仅含构建命令）
            |-- summarize-task.md     独立（仅含报告模板）
            |-- extract-harness-tpl.md 读取全部 .harness/ 文件
            |
Layer 3  .harness/skills/subskills/（Subskill 任务模板 -- "做什么"）
            |
            |-- scan-*.md  引用源码路径，检查规则来自 AGENTS.md/03-conventions.md
            |              被 reviewer.md 和 governance-code.md 调用
            |
数据层   .harness/context/（知识库） + .harness/guides/（方法论）
            |
            |-- context/agents/01-overview.md     指回 AGENTS.md（"操作约束见 AGENTS.md"）
            |-- context/agents/03-conventions.md  指回 AGENTS.md（声明自己是权威源，AGENTS.md为摘要）
            |-- context/agents/02,04,05,06,07     独立数据文档，不引用其他 .harness 文件
            |-- context/users/01,02,03-prd-*.md   独立产品文档，AI只读
            |-- guides/00-harness-desc.md         通用方法论，人工维护
            |-- guides/01-harness-ops.md          项目维护手册，人工维护
            |-- guides/02-harness-dev.md          开发流程，人工维护
```
