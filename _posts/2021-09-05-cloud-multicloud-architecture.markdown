---
layout: post
title: 基于云原生的多云架构
date: 2021-09-05 22:00
tags:
  - thoughts
---

## 导读
本文主要介绍了CH公司的云原生多云架构体系，包括云原生、多云两个部分。下文中，公司名称简称为CH。

## 架构全貌
CH基于云原生的多云架构，如下图：

![multicloud-architecture](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20210905/multicloud-architecture.png)

其中，关键点包括专线互通、容器环境交付、数据同步、流量分区等，辅助因素包括多云资源管控、多云容器管理、服务治理体系、应用运营体系等。

