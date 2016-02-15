---
layout: post
title: 一种松耦合的运维系统设计
date: 2016-02-16 00:00
tags:
  - system
---


工作以来，一直坚信"平台化、易复用"的设计理念。在阿里、小米，先后见识了不少运维子系统，多多少少都和业务耦合、被业务所累，几乎找不到一个可以轻松移植的子系统。本文尝试提出一种松耦合的运维系统设计思路，纯属个人YY、当前没有实践做支撑。


## 概述
为什么，要以松耦合的方式，构建运维体系呢？很简单，方便运维子系统的复用。最好能做到，运维子系统 可以轻易接入 不同公司的运维体系。

怎样，才能让运维系统，松耦合的发生关联呢？运维系统，包含众多子系统，各子系统分别负责不同的运维业务。子系统之间往往"取长补短"、相互依赖，如Deploy需要CMDB的服务器信息才能完成部署业务、Monitor需要ACL才能完成数据的准入&准出等等。**只要遵循统一的协议，子系统就可以享受其他子系统提供的服务；如果这个协议可以封装公司的业务属性，那么各子系统就可以蜕化成纯平台、进而可以跨公司复用**——这正是本文的设计思路。


## 业务树
想来想去，**业务树**是最适合的协议平台。一方面，很多公司的运维体系以传统的服务树为核心展开，不同的子系统都挂载到服务树；服务树成为运维系统的统一portal(很多时候，我们把服务树当成CMDB的一种展示形态，略狭隘)。另一方面，以树状结构抽象公司的业务逻辑，已经证明是一条可行的道路。这样，业务树就成了本文 松耦合运维系统 的核心。

不妨下一个定义: **业务树，是公司业务的抽象，是统一的协议平台，是独立存在的实体**。请注意，业务树是独立的实体，不是CMDB的"附庸"! 

一棵典型的业务树，如下，
![business_tree.png](https://raw.githubusercontent.com/niean/niean.common.store/master/images/devops/rbac/tree.png)

不同公司，业务树的组织形式、描述方式不尽相同。为了屏蔽差异、实现复用，我们用字符串来描述一个业务树节点，通过字符串之间的包含关系来确定节点的父子关系。上述业务树，可以描述如下，

|ID|Name|Comment|
|:----|:----|:----|:----|
|0|`cop.tycs`|公司,tycs|
|1|`cop.tycs_owt.inf`|团队,inf|
|2|`cop.tycs_owt.inf_pdl.falcon`|产品线,falcon|
|3|`cop.tycs_owt.inf_pdl.falcon_service.dashboard`|服务,dashboard|
|4|`cop.tycs_owt.inf_pdl.falcon_service.gateway`|服务,gateway|
|5|`cop.tycs_owt.inf_pdl.falcon_service.gateway_job.gateway`|作业,gateway|
|6|`cop.tycs_owt.inf_pdl.falcon_service.gateway_job.gateway_cluster.aws-de`|集群,aws-de|

举个例子，`cop.tycs_owt.inf`是`cop.tycs`的子节点，因为前者"字符串包含"后者。我们可以用ID去表示一个树节点，也可以用节点名称Name，这完全取决于子系统的业务需要(当然,最终需要将ID或者Name适配成统一形式)。

上述，只是业务树的一种表示形式，不同公司可以使用自己特有的业务树描述方式。


## 接入

#### Monitor + CMDB

#### Monitor + ACL

#### Deploy + CMDB



