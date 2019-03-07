---
layout: post
title: 监控定位体系建设思路
date: 2019-03-06 11:10
tags:
  - thoughts
---

## 导读
监控体系的职责是**提供快速发现和定位故障的能力**。本文首先介绍了一次典型的故障处理流程，然后给出了一种监控定位体系的建设思路。

## 典型的故障处理流程
一次典型的故障处理过程如下图所示，

![page.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20190306/process.png)

对于比较简单的故障，定位过程可能会跳过业务、接口、模块三个层次，直接到实例级别。

## 监控定位体系建设思路
围绕发现、定位两个核心能力，结合上下游依赖、时间两个维度，将监控体系划分为业务监控、应用监控、基础监控三个层次。如下图所示，

![page.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20190306/monitor.system.png)

监控系统的产品能力输出，一般表现为 报警通知、红绿灯看板、同环比看板、统计表格、事件墙等。所有的产品设计，都是为了实现快速发现、快速定位。

未完待续(需要再细化下监控定位体系各个环节的关键点)...

