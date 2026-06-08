<!-- SUMMARY: 博客文章、草稿、页面、配置与磁盘存储结构的数据边界。 -->
# 数据与类型边界

## 核心数据模型

本项目为静态博客，核心数据为文章，由 Jekyll 管理：

### 文章（Post）

```yaml
# Front Matter 示例
---
layout: post
title: 文章标题
date: 2024-01-01
categories: [分类1, 分类2]
tags: [标签1, 标签2]
---
```

必需字段：
- layout：布局模板，通常为 post
- title：文章标题
- date：发布日期

可选字段：
- categories：文章分类（数组）
- tags：文章标签（数组）

### 草稿（Draft）

与文章结构相同，但存放在 _drafts/ 目录。本项目草稿文件沿用与文章相同的日期前缀命名（如 YYYY-MM-DD-title.markdown）。

### 页面（Page）

```yaml
---
title: 页面标题
layout: page
---
```

## 配置结构

### _config.yml 核心配置

```yaml
markdown: kramdown      # Markdown 解析器
author: niean           # 作者
name: "田园木竹"         # 博客名称
url: http://blog.niean.name  # 博客地址
permalink: /:year/:month/:day/:title  # 文章 URL 格式
paginate: 16            # 分页大小
giscus:                 # Giscus 评论配置
  repo: niean/niean.github.io
  mapping: pathname
collections:
  drafts:
    output: true        # 草稿输出为页面
    permalink: /drafts/:year/:month/:day/:title/
```

## 磁盘存储结构

```
_posts/
  YYYY-MM-DD-title.markdown    # 已发布文章
_drafts/
  YYYY-MM-DD-title.markdown    # 草稿文章（本项目带日期前缀）
images/
  YYYYMMDD/                    # 按日期组织的图片目录
resource/
  YYYYMMDD/                    # 按日期组织的资源目录
_site/                         # 构建输出目录（git ignored）
```

## 边界约定

- 文章数据由 Jekyll 在构建时解析，无需运行时数据库
- 图片资源按文章日期组织，便于管理
- 构建产物 _site/ 不纳入版本控制
- Valine 历史评论导出 blog-comments.json 含评论内容、IP、邮箱、UA 等原始数据，不纳入版本控制
