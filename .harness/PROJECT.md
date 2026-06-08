# PROJECT.md -- niean's blog

个人技术博客，记录运维、SRE、架构、研发效能等领域实践与思考。

---

# Harness 框架适配

本节为 Harness 框架提供项目级配置，框架文件通过 `.harness/PROJECT.md` 直接引用。

## 知识库目录

首次加载时需建立 SUMMARY 索引的目录：
- `.harness/knowledge/`
- `.harness/prd/`（除 .harness/prd/03-prd-specs.md）
- `.harness/lessons/`

## 任务类型加载矩阵

首次加载时，根据任务类型选择性读取知识库文件（所有文件首行 SUMMARY 始终必读）：

| 任务类型 | 必读（完整读取） | 按需读取 |
|---------|----------------|---------|
| 功能需求 | .harness/knowledge/01-overview.md, .harness/knowledge/02-architecture.md, .harness/knowledge/22-file-map.md, .harness/prd/01-prd-sense.md, .harness/prd/02-prd-baseline.md | .harness/knowledge/03-conventions.md, .harness/knowledge/04-data-boundaries.md, .harness/knowledge/05-key-patterns.md, .harness/knowledge/21-glossary.md |
| 功能精调 | .harness/knowledge/01-overview.md, .harness/knowledge/22-file-map.md | .harness/knowledge/02-architecture.md, .harness/knowledge/03-conventions.md, .harness/knowledge/04-data-boundaries.md, .harness/knowledge/05-key-patterns.md, .harness/knowledge/21-glossary.md |
| Bug修复 | .harness/knowledge/01-overview.md, .harness/knowledge/03-conventions.md, .harness/knowledge/22-file-map.md | .harness/knowledge/02-architecture.md, .harness/knowledge/04-data-boundaries.md, .harness/knowledge/05-key-patterns.md, .harness/knowledge/21-glossary.md |
| 治理/扫描 | .harness/knowledge/01-overview.md, .harness/knowledge/03-conventions.md, .harness/knowledge/22-file-map.md | .harness/knowledge/02-architecture.md, .harness/knowledge/05-key-patterns.md |
| 文档维护 | .harness/knowledge/01-overview.md, .harness/knowledge/22-file-map.md | 读取目标文件引用链上的 knowledge/ 和 prd/ 文件 |

## 知识回填文件映射

知识回填的回填目标：
- 架构变化 -> .harness/knowledge/02-architecture.md
- 新术语 -> .harness/knowledge/21-glossary.md
- 数据结构/存储变化 -> .harness/knowledge/04-data-boundaries.md
- 新源文件 -> .harness/knowledge/22-file-map.md
- 新跨文件模式 -> .harness/knowledge/05-key-patterns.md
- 产品方向调整 -> 提示用户，人工更新 .harness/prd/01-prd-sense.md

## 教训库加载路径

本项目教训库分布在两个位置：
- `.harness/framework/lessons/general.md`（Harness 通用教训）
- `.harness/lessons/project.md`（项目教训）

## 构建与测试

### 构建
```bash
jekyll build
```

### 单元测试
单元测试执行策略：
- 用户明确要求时：必须执行
- 本项目为静态博客，无自动化单元测试；常规质量保障以构建验证为主
- 其他场景：跳过

```bash
jekyll build
```

## 扫描维度

代码扫描使用的维度及规则来源。下表路径均相对于 `.harness/knowledge/` 目录：

| # | 维度 | 规则来源 |
|---|------|---------|
| 1 | 文章格式与 Front Matter | 03-conventions.md, 04-data-boundaries.md |
| 2 | Jekyll 模板与 Liquid 约定 | 03-conventions.md, 05-key-patterns.md |
| 3 | 资源路径与文件组织 | 02-architecture.md, 04-data-boundaries.md, 22-file-map.md |
| 4 | 链接与安全约束 | 03-conventions.md |
| 5 | 构建可用性 | 03-conventions.md |

可选（涉及文件删除时）：

| # | 维度 | 规则来源 |
|---|------|---------|
| 6 | 删除影响范围 | 22-file-map.md, 02-architecture.md |

## 项目知识索引

| 文件 | 何时查阅 |
|------|---------|
| .harness/prd/01-prd-sense.md | 功能迭代前，确认产品定位和判断准则 |
| .harness/knowledge/01-overview.md | 任务开始时，了解项目概览（技术栈/入口/核心流程） |
| .harness/knowledge/02-architecture.md | 涉及模块新增、目录边界、页面结构调整时 |
| .harness/knowledge/03-conventions.md | 涉及编码、文章格式、质量、安全约定细节时 |
| .harness/knowledge/04-data-boundaries.md | 涉及 Front Matter、配置、磁盘存储结构时 |
| .harness/knowledge/05-key-patterns.md | 实现文章创建、布局继承、include 复用、资源组织模式时 |
| .harness/knowledge/21-glossary.md | 对 Jekyll、博客、项目术语不清楚时 |
| .harness/knowledge/22-file-map.md | 确定功能对应源文件时 |
| .harness/prd/02-prd-baseline.md | 确认功能需求与产品约束时 |
| .harness/lessons/project.md | 用户指令或当前根因与 SUMMARY 高度相关时按需读取 |

---

# 项目规范

## 代码生成

以下各节（代码生成、架构边界、质量守护、安全规范）为快速参考摘要，权威定义见 .harness/knowledge/03-conventions.md。

- Liquid 模板：使用 Liquid 模板语法，遵循 Jekyll 规范
- Markdown 文章：使用 kramdown 解析，文章头部必须包含 YAML Front Matter
- 文章命名：已发布文章文件名使用 YYYY-MM-DD-title.markdown 或 YYYY-MM-DD-title.md
- 图片资源：存放于 images/ 目录，按文章日期组织子目录
- 本地化：博客主要使用中文，技术文章可包含英文术语和代码

## 架构边界

本项目为静态博客站点，架构简单：
- 表现层：HTML 模板（_layouts/、_includes/）
- 内容层：Markdown 文章（_posts/、_drafts/）
- 配置层：Jekyll 配置（_config.yml）
- 资源层：静态文件（images/、media/、resource/）

## 质量守护

- 构建验证：执行 `jekyll build` 确保无错误
- 文章格式：符合 Markdown 规范，Front Matter 完整
- 链接检查：确保内部链接有效
- 部署检查：关注 GitHub Pages 部署状态

## 安全规范

- 不在文章中泄露敏感信息（密钥、密码、内网地址等）
- 外部链接使用 `rel="noopener noreferrer"` 属性
- 如有评论系统，需防范 XSS 攻击
- GitHub Pages 部署时自动启用 HTTPS

---

# 项目附录

## 仓库结构

```text
AGENTS.md              -- AI 入口（纯路由）
CLAUDE.md              -- Claude Code 入口
.harness/
  PROJECT.md           -- 项目规范入口
  framework/           -- 通用能力
  knowledge/           -- AI 知识库（01~05 认知约束类, 21~22 工具索引类）
  prd/                 -- 产品文档（AI只读：01-prd-sense、02-prd-baseline、03-prd-specs）
  lessons/
    project.md         -- 项目教训（AI自主维护）
  specs/               -- 设计文档
    active/
    completed/
  plans/               -- 实现计划
    active/
    completed/
    debt-tracker.md    -- 技术债追踪
_config.yml            -- Jekyll 配置文件
_includes/             -- Jekyll 模板片段
_layouts/              -- Jekyll 布局模板
_posts/                -- 已发布的博客文章
_drafts/               -- 草稿文章
images/                -- 博客图片资源
media/                 -- 静态资源（CSS/JS/Fonts）
resource/              -- 其他资源文件
about/                 -- 关于页面
archives/              -- 归档页面
categories/            -- 分类页面
tags/                  -- 标签页面
drafts/                -- 草稿列表页面
paginator/             -- 分页页面
```

## 知识层级关系

```text
Layer 0   AGENTS.md -> FRAMEWORK.md（通用规范+注册表） + PROJECT.md（项目配置+规则摘要）
Layer 1   framework/agents/（5个角色: Orchestrator/Designer/Planner/Coder/Reviewer）
Layer 1.5 framework/workflows/（迭代功能/修复Bug/迭代文档 + harness-ops/治理类）
Layer 2   framework/skills/（harness/ 核心Skill + harness-ops/ 运维Skill + superpowers/ 方法论）
Layer 3   framework/skills/harness/subskills/（扫描模板）
数据层    knowledge/（权威知识） + prd/（产品文档，AI只读） + guides/（方法论） + lessons/（教训）
辅助层    specs/（设计文档） + plans/（执行计划+技术债）
```

引用方向：Layer 0 -> Layer 1/1.5 -> Layer 2 -> Layer 3 -> 数据层。PROJECT.md 摘要引用 knowledge/03-conventions.md（权威源）。
