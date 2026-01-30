---
title: 标签
layout: page
---

{% assign tags_array = '' | split: '' %}
{% for tag in site.tags %}
  {% assign tag_name = tag[0] %}
  {% assign tag_posts = tag[1] %}
  {% assign sorted_tag_posts = tag_posts | sort: 'date' | reverse %}
  {% assign latest_post = sorted_tag_posts | first %}
  {% if latest_post.date %}
    {% assign latest_date = latest_post.date | date: "%Y%m%d" %}
  {% else %}
    {% assign latest_date = "00000000" %}
  {% endif %}
  {% assign tag_entry = latest_date | append: '||' | append: tag_name %}
  {% assign tags_array = tags_array | push: tag_entry %}
{% endfor %}
{% assign sorted_tags_array = tags_array | sort | reverse %}

<div id='tag_cloud'>
  {% for tag_entry in sorted_tags_array %}
    {% assign tag_parts = tag_entry | split: '||' %}
    {% assign tag_name = tag_parts[1] %}
    {% assign tag = site.tags[tag_name] %}
    <a href="#{{ tag_name }}" title="{{ tag_name }}" rel="{{ tag.size }}">{{ tag_name }}({{ tag.size }})</a>
  {% endfor %}
</div>

<ul class="listing">
  {% for tag_entry in sorted_tags_array %}
    {% assign tag_parts = tag_entry | split: '||' %}
    {% assign tag_name = tag_parts[1] %}
    {% assign tag = site.tags[tag_name] %}
    <li class="listing-seperator" id="{{ tag_name }}">{{ tag_name }}</li>
    {% assign sorted_posts = tag | sort: 'date' | reverse %}
    {% for post in sorted_posts %}
    <li class="listing-item">
      <time datetime="{{ post.date | date:"%Y-%m-%d" }}">{{ post.date | date:"%Y-%m-%d" }}</time>
      <a href="{{ site.url }}{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a>
    </li>
    {% endfor %}
  {% endfor %}
</ul>

<script src="/media/js/jquery.tagcloud.js" type="text/javascript" charset="utf-8"></script> 
<script language="javascript">
$.fn.tagcloud.defaults = {
    size: {start: 1, end: 2, unit: 'em'},
    color: {start: '#f8e0e6', end: '#ff3333'}
};

$(function () {
    $('#tag_cloud a').tagcloud();
});
</script>
