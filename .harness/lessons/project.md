<!-- SUMMARY: {{项目名称}}开发中的经验教训，AI自主维护 -->
# 项目教训

AI 自主维护，人工可通过提示或建议触发新增/修正。
项目教训绑定{{项目名称}}，不随 Harness 模板提取。

---

### P001: details 折叠内 Markdown 不渲染

- 现象：文章中 `<details>` 折叠块内的 fenced code block、列表、行内代码均不渲染；反引号原样输出，闭合 `</details>` 被转义为 `&lt;/details&gt;`，代码块内的伪 XML（如 `<memory-context>`）被当成真实 HTML 元素破坏页面结构；`<details>` 内的 mermaid 图表也不渲染。
- 根因：kramdown 默认将块级 HTML 元素（`<details>`、`<div>` 等）内容视为原始 HTML，不解析其中的 Markdown，需给标签加 `markdown="1"` 属性才会解析。mermaid 不渲染是同一根因的下游表现：kramdown 未把 mermaid 围栏块转为 `<code class="language-mermaid">`，`_includes/mermaid.html` 的 JS（匹配 `code.language-mermaid`）无目标可转换。根因追踪涉及 _posts 文章、_config.yml（markdown: kramdown）、_includes/mermaid.html 三处。
- 教训：在 `<details>` 等块级 HTML 内放 Markdown 内容时，必须加 `markdown="1"` 属性（`<details markdown="1">`），并在 `</summary>` 后留空行；若内部仅放原生 HTML（如 `<pre><code>`）则不需要。已沉淀为 knowledge/05-key-patterns.md 模式五。
- 来源：plan N/A（fix-bug），_posts/2026-07-04-ai-nagent.md

### P002: mermaid 图表标签被大写

- 现象：mermaid 图表中的状态名、边标签等小写文本被渲染为大写（如 `active` 显示为 `ACTIVE`）。
- 根因：mermaid @10 通过 `attr("class","label")` 给 SVG 标签元素赋 `label` class；博客全局 `.label` 徽章规则（style.css、home.css，原为 UI 标签徽章设计）含 `text-transform:uppercase`，级联进入 mermaid SVG。SVG 忽略 `background-color`/`padding`/`border-radius`，mermaid 主题覆盖 `color`/`font`，但 `text-transform` 无任何来源覆盖，故被大写。根因追踪涉及 media/css/style.css、media/css/home.css、_includes/mermaid.html、mermaid@10 JS（class 赋值）。
- 教训：第三方库（mermaid）使用的 class 名（`label`）可能与项目全局 CSS 命名空间碰撞；排查“文本大小写异常”时优先查 `text-transform` 级联。修复用作用域覆盖 `.mermaid .label { text-transform: none; }`（特异性 0,2,0 > 0,1,0）。已沉淀为 knowledge/05-key-patterns.md 模式六。
- 来源：plan N/A（fix-bug），_includes/mermaid.html
