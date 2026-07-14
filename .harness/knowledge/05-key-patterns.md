<!-- SUMMARY: 博客文章创建、布局继承、模板片段复用与资源组织的关键模式。 -->
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
- 评论当前通过 _includes/comments.md 加载 Giscus，配置集中在 _config.yml 的 giscus 字段
- Valine 旧实现保留在 _includes/comments-valine-legacy.md，默认不引用
- 每篇文章通过 .github/scripts/giscus_ensure_discussions.py 预创建 discussion（title=term），避免页面加载时 giscus 返回 404；本地 --execute 回填、CI（.github/workflows/giscus-ensure-discussions.yml）push _posts/ 时自动补建

陷阱：
- include 文件路径相对于 _includes/ 目录
- 传入参数使用 `{% include filename param=value %}`
- Giscus mapping=pathname、strict=0：giscus term = window.location.pathname 去首尾斜杠 = yyyy/mm/dd/slug；discussion title 用此 term（giscus 原生格式）。strict=0 为包含匹配，历史迁移的 /yyyy/mm/dd/slug/（带斜杠）与 giscus 原生 yyyy/mm/dd/slug（无斜杠）两种 title 均能被命中
- Giscus 页面展示 Discussion comments，历史归档需写入 comment；仅写在 Discussion body 中不会作为文章下方历史评论展示

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

## 模式五：HTML 块内嵌 Markdown

描述：在 `<details>` 等块级 HTML 元素内放置 Markdown 内容（fenced code block、列表、行内代码等）时，需显式启用 kramdown 的 Markdown 解析。

实现要点：
- 给块级 HTML 标签添加 `markdown="1"` 属性，如 `<details markdown="1">`
- `</summary>` 与首个 Markdown 块之间保留一个空行，确保 Markdown 块被正确识别
- 启用后 kramdown 将解析内部 Markdown：fenced code block 转为 `<pre><code>`、列表转为 `<ul>`、行内代码转为 `<code>`

陷阱：
- kramdown 默认将块级 HTML 元素（如 `<details>`、`<div>`）内容视为原始 HTML，不解析 Markdown；此时 fenced code block 的反引号原样输出，闭合 `</details>` 可能被转义为 `&lt;/details&gt;`，内部伪 XML（如示例中的 `<memory-context>`）会被当成真实 HTML 元素，破坏页面结构
- mermaid 图表放在 `<details>` 内时同样依赖 `markdown="1"`：只有 kramdown 把 mermaid 围栏代码块转为 `<code class="language-mermaid">`，`_includes/mermaid.html` 的 JS（匹配 `code.language-mermaid`）才能识别并渲染图表
- 若 `<details>` 内仅放原生 HTML（如 `<pre><code>`，见 se-ddd 文章样例），则无需 `markdown="1"`

涉及文件：_posts/（文章正文）、_includes/mermaid.html（mermaid 渲染依赖该模式生成的 code.language-mermaid）

## 模式六：mermaid 标签 CSS 命名冲突

描述：mermaid 渲染的 SVG 标签元素带 `label` 等 class，与博客全局 `.label` 徽章样式冲突，导致图表标签被大写。

实现要点：
- mermaid @10 通过 `attr("class","label")` 为状态名、边标签等 SVG 元素赋 `label` class
- 博客 `.label` 规则（style.css、home.css）原为 UI 徽章设计，含 `text-transform:uppercase`
- SVG 忽略 `background-color`/`padding`/`border-radius`，mermaid 主题覆盖 `color`/`font`，但 `text-transform` 无覆盖，故标签被大写
- 修复：在 `_includes/mermaid.html` 的 `<style>` 块加作用域覆盖 `.mermaid .label { text-transform: none; }`，特异性 (0,2,0) > `.label` (0,1,0)，不影响博客其它 `.label` 徽章用法

陷阱：
- 该冲突影响所有 mermaid 图表，不仅限于 `<details>` 内的
- 排查时易误以为是 mermaid 主题或 kramdown 问题，实为博客 CSS 与 mermaid class 命名空间碰撞

涉及文件：_includes/mermaid.html（覆盖规则）、media/css/style.css 与 media/css/home.css（全局 .label 徽章规则）
