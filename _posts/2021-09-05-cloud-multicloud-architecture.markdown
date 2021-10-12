---
layout: post
title: 云原生之多云架构
date: 2021-09-05 22:00
tags:
  - thoughts
---

## 导读
本文主要介绍了CH公司的云原生多云架构体系，包括云原生、多云两个部分。下文中，公司名称简称为CH。

## 架构全貌
CH基于云原生的多云架构，如下图：

![multicloud-architecture](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20210905/multicloud-architecture.png)

其中，关键功能包括专线互通、基于容器技术的环境交付、数据同步、流量分区等，关键技术包括多云的资源管理、容器技术、服务治理、服务管理等。

## 容器技术
关键点包括：

- 镜像技术
- 运行时
- 作业编排
- 作业调度

## 服务治理
关键点包括：

- 服务注册/发现
- 服务通信
- 流量管控
- 服务观察

