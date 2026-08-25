---
title: 不公开
layout: page
permalink: /unposts/
---

<ul class="listing">
{% assign unposts_to_sort = site.unposts %}
{% if unposts_to_sort and unposts_to_sort.size > 0 %}
  {% assign sorted_unposts = unposts_to_sort | sort: 'date' | reverse %}
  {% for unpost in sorted_unposts %}
    {% if unpost.date %}
      {% capture y %}{{unpost.date | date:"%Y"}}{% endcapture %}
      {% if year != y %}
        {% assign year = y %}
        <li class="listing-seperator">{{ y }}</li>
      {% endif %}
      <li class="listing-item">
        <time datetime="{{ unpost.date | date:"%Y-%m-%d" }}">{{ unpost.date | date:"%Y-%m-%d" }}</time>
        <a href="{{ unpost.url }}" title="{{ unpost.title }}">{{ unpost.title }}</a>
      </li>
    {% endif %}
  {% endfor %}
{% endif %}
</ul>
