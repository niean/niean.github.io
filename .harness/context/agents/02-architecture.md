# 架构与模块边界

## 分层

本项目为静态博客站点，采用典型的 Jekyll 静态站点架构：

- 表现层：HTML 模板（_layouts/、_includes/）
- 内容层：Markdown 文章（_posts/、_drafts/）
- 配置层：Jekyll 配置（_config.yml）
- 资源层：静态文件（images/、media/）

## 模块边界

| 模块 | 目录 | 职责 |
|------|------|------|
| 布局模板 | _layouts/ | 页面布局模板（default、page、post） |
| 模板片段 | _includes/ | 可复用的模板片段（comments、pay） |
| 已发布文章 | _posts/ | 已发布的博客文章 |
| 草稿文章 | _drafts/ | 未发布的草稿文章 |
| 图片资源 | images/ | 博客文章配图，按日期目录组织 |
| 静态资源 | media/ | CSS、JS、Fonts 等静态资源 |
| 页面 | about/、archives/、categories/、tags/、drafts/、paginator/ | 各功能页面 |
| 其他资源 | resource/ | 文章附带的资源文件（如 Excel、PPT） |

## 关键约束

- _posts/ 文件命名必须遵循 YYYY-MM-DD-title.markdown 格式
- 所有文章必须包含 YAML Front Matter（layout、title、date 等）
- 图片资源按文章日期组织目录（如 images/20150806/）
- _config.yml 中配置的 collections 定义了 drafts 集合