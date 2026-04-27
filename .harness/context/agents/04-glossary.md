# 术语表

## Jekyll 相关

- Jekyll：静态站点生成器，将 Markdown 文件转换为静态 HTML 网站
- Liquid：Ruby 模板语言，Jekyll 使用其处理模板
- kramdown：Markdown 解析器，Jekyll 默认使用
- Front Matter：文章头部的 YAML 元数据块，以 `---` 分隔
- Layout：页面布局模板，定义页面结构
- Include：可复用的模板片段
- Collection：Jekyll 的内容集合，如 posts、drafts
- Permalink：文章的 URL 格式定义

## 博客相关

- Post：博客文章，存放于 _posts/ 目录
- Draft：草稿文章，存放于 _drafts/ 目录
- Page：静态页面，如关于页面、归档页面等
- Category：文章分类
- Tag：文章标签
- Paginator：分页器，用于文章列表分页

## 项目特有

- 田园木竹：博客名称，来自 _config.yml 中的 name 字段
- niean：博客作者，来自 _config.yml 中的 author 字段
- blog.niean.name：博客域名，配置于 _config.yml 和 CNAME 文件