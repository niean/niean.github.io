<!-- SUMMARY: Jekyll 博客的 UI、编码、质量、文件管理与安全约定。 -->
# 约定与约束（实现细节）

本文件是项目规范约定的权威来源，`.harness/PROJECT.md` 为摘要引用，以本文件为准。

---

# 一、UI交互约定

本项目为静态博客，无复杂UI交互，主要遵循以下约定：

- 页面布局基于 Jekyll 模板系统，使用 Liquid 语法
- 样式通过 media/css/ 下的 CSS 文件定义
- 字体资源位于 media/fonts/
- JavaScript 脚本位于 media/js/

---

# 二、编码约定

## Liquid 模板

- 使用 Liquid 模板语法，遵循 Jekyll 规范
- 模板文件使用 .html 扩展名（如 _layouts/default.html）
- 变量使用双花括号语法：`{{ variable }}`
- 标签使用花括号百分号语法：`{% tag %}`

## Markdown 文章

- 使用 kramdown 解析器
- 文章头部必须包含 YAML Front Matter，以 `---` 分隔
- 必需字段：layout（通常为 post）、title、date
- 文件名格式：YYYY-MM-DD-title.markdown 或 YYYY-MM-DD-title.md
- 文章正文使用标准 Markdown 语法

## 图片/媒体处理

- 图片存放于 images/ 目录，按文章日期组织子目录
- 图片命名使用小写英文，可包含数字和连字符
- 支持格式：png、jpg、jpeg、gif 等
- 资源文件（如 Excel、PPT）存放于 resource/ 目录

## 数据格式

- 配置文件使用 YAML 格式
- 站点配置：_config.yml
- Front Matter 使用 YAML 语法

## 本地化

- 博客主要使用中文
- 技术文章可包含英文术语和代码

---

# 三、质量约定

## 编译

构建命令：`jekyll build`

提交前执行构建验证，确保无错误。

## 错误处理

- 构建错误：根据 Jekyll 错误信息定位并修复
- Front Matter 错误：检查 YAML 语法和必需字段
- Liquid 语法错误：检查模板语法

## 日志

Jekyll 构建时会在终端输出日志，注意检查警告和错误信息。

## 单元测试

本项目为静态博客，无自动化测试。质量保障主要依赖：
- 本地构建验证
- 本地预览检查
- GitHub Pages 部署状态

---

# 四、文件管理约定

- 禁止主动创建 README
- 不删除项目文件（临时 spec 除外）
- 文件名：小写英文 kebab-case，动词-名词语序
- 临时计划落盘到 `.harness/plans/`
- 本地临时草稿与扫描中间产物落盘到 `locals/harness_tmp/`

---

# 五、安全约定

- 不在文章中泄露敏感信息（密钥、密码、内网地址等）
- 外部链接使用 `rel="noopener noreferrer"` 属性
- 如有评论系统，需防范 XSS 攻击
- GitHub Pages 部署时自动启用 HTTPS
