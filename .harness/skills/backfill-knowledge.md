# Skill: 回填知识库

触发：人工指令。对比实际代码与知识库文档，修正过时描述并同步 AGENTS.md。

本 Skill 采用单 Agent 架构，由主 Agent 直接执行。

## 步骤

### Step 1 -- 读取现状
读取 AGENTS.md + .harness/context/agents/ 全部 + context/users/ 目录结构 + skills/ 目录（含 subskills/），按需扫描源码目录。

### Step 2 -- 更新 agents/ 知识库
对比实际代码与文档，修正过时描述，简化压缩内容。

### Step 3 -- 提取 AGENTS.md 候选变更
识别：仓库结构不一致、Skills/Subskills 表过时、知识库索引不一致、摘要与 03-conventions.md 不同步等。列出候选清单（位置、当前描述、建议描述、原因）。

### Step 4 -- 等待人工确认
通过 ask_followup_question 展示候选清单（必须写在 question 参数内）。

### Step 5 -- 更新 AGENTS.md
按确认项最小化修改。

### Step 6 -- 输出变更摘要
