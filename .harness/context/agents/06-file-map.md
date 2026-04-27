# 功能与文件映射

## 站点入口与全局

- 站点配置：_config.yml
- 首页文章列表：index.html
- Atom Feed：atom.xml
- 域名配置：CNAME

## 布局模板

- 默认布局：_layouts/default.html
- 页面布局：_layouts/page.html
- 文章布局：_layouts/post.html

## 模板片段

- 评论组件：_includes/comments.md
- 打赏组件：_includes/pay.md

## 内容目录

- 已发布文章：_posts/*.markdown
- 草稿文章：_drafts/*.markdown

## 功能页面

- 关于页面：about/index.md
- 归档页面：archives/index.md
- 分类页面：categories/index.md
- 标签页面：tags/index.md
- 草稿列表：drafts/index.md
- 分页页面：paginator/index.html

## 资源目录

- 图片资源：images/（按日期组织子目录）
- 静态资源：media/css/、media/js/、media/fonts/
- 其他资源：resource/（文章附带的 Excel、PPT 等）

## 构建输出

- 构建产物：_site/（不纳入版本控制）