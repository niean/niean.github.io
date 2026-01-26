---
title: 草稿
layout: page
---

<ul class="listing">
{% assign drafts_to_sort = site.drafts %}
{% if drafts_to_sort and drafts_to_sort.size > 0 %}
  {% assign sorted_drafts = drafts_to_sort | sort: 'date' | reverse %}
  {% for draft in sorted_drafts %}
    {% if draft.date %}
      {% capture y %}{{draft.date | date:"%Y"}}{% endcapture %}
      {% if year != y %}
        {% assign year = y %}
        <li class="listing-seperator">{{ y }}</li>
      {% endif %}
      <li class="listing-item">
        <time datetime="{{ draft.date | date:"%Y-%m-%d" }}">{{ draft.date | date:"%Y-%m-%d" }}</time>
        <a href="{{ draft.url }}" title="{{ draft.title }}">{{ draft.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
{% endif %}
</ul>
