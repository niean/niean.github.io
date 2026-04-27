# 项目概览

## 一句话

niean的个人博客，记录运维、SRE、架构等领域实践与思考。

## 技术栈

- 静态站点生成器：Jekyll
- 模板引擎：Liquid
- Markdown解析器：kramdown
- 代码高亮：无（pygments: false）
- 部署平台：GitHub Pages
- 分页插件：jekyll-paginate

## 入口与根状态

- 站点入口：index.html（博客文章列表页）
- 配置文件：_config.yml
- 布局模板：_layouts/目录（default.html、page.html、post.html）

## 核心流程

1. 创建文章：在 _posts/ 目录创建 YYYY-MM-DD-title.markdown 文件
2. 编写内容：添加 YAML Front Matter，撰写 Markdown 正文
3. 本地预览：执行 `jekyll serve` 本地预览
4. 构建部署：执行 `jekyll build` 生成静态文件到 _site/
5. 发布上线：推送到 GitHub，由 GitHub Pages 自动部署

## 文档与规则

操作约束、知识库加载策略见根目录 AGENTS.md。