# 关键代码模式

项目中反复出现但不易从单个文件推断的模式，供新功能实现时参照。

## 模式一：文章创建

描述：创建新博客文章的标准流程。

实现要点：
- 在 _posts/ 目录创建文件，命名格式 YYYY-MM-DD-title.markdown
- 添加 YAML Front Matter，包含 layout、title、date 必需字段
- 使用 Markdown 编写正文内容
- 如有图片，存放至 images/YYYYMMDD/ 目录

陷阱：
- 文件名日期与 Front Matter 日期需保持一致
- Front Matter 必须以 `---` 开头和结尾

涉及文件：_posts/

## 模式二：布局继承

描述：页面模板继承 default 布局，添加特定内容。

实现要点：
- 创建新页面时，在 Front Matter 中指定 layout
- default.html 是基础布局，包含 HTML 结构和公共部分
- page.html 和 post.html 继承 default 布局

陷阱：
- 新布局需放在 _layouts/ 目录
- 使用 `{{ content }}` 插入子模板内容

涉及文件：_layouts/default.html、_layouts/page.html、_layouts/post.html

## 模式三：模板片段复用

描述：通过 include 复用模板片段。

实现要点：
- 将可复用片段存放于 _includes/ 目录
- 使用 `{% include filename %}` 引入片段
- 常用于评论、打赏、页头、页脚等公共部分

陷阱：
- include 文件路径相对于 _includes/ 目录
- 传入参数使用 `{% include filename param=value %}`

涉及文件：_includes/

## 模式四：资源组织

描述：文章配套资源的组织方式。

实现要点：
- 图片存放于 images/YYYYMMDD/ 目录
- 其他资源存放于 resource/YYYYMMDD/ 目录
- 在文章中使用相对路径引用

陷阱：
- 图片目录按文章发布日期命名，而非创建日期
- 大文件需考虑 GitHub 仓库大小限制

涉及文件：images/、resource/