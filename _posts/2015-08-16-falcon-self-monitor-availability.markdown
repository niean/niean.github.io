---
layout: post
title: 小米监控系统Falcon的自监控（1）
date: 2015-08-16 18:00
tags:
  - monitor
  - falcon
---

通常，监控系统被用于发现其他服务系统的故障。那么，监控系统自身发生故障时，谁来发现这件事呢？监控系统的自监控怎么搞？我们介绍了小米监控系统Falcon的一些自监控实践，希望对大家有所帮助。

高大上的讲，Falcon的自监控有两个维度: 故障发现 和 故障预判。故障发现指的是，当Falcon某个组件实例不可用时，自监控服务能够及时发现该故障，并通知相应的运维人员。故障预判指的是，通过自监控服务，能够预测出Falcon组件即将发生的故障，并把即将发生的故障通知到相应的运维人员。我们还没有进化到故障自动恢复的阶段，甚至故障预判的主要逻辑都需要人来完成。

本文主要介绍Falcon"故障发现"的实现，"故障预判"的内容，将在下一篇文章中介绍。

Falcon各模块，提供服务状态API。通过该API，可以获知该服务是否正常。

自监控组件AntEye，定期主动查询Falcon各模块实例的服务状态，然后根据报警规则判断是否报警。Falcon模块的所有实例，在AntEye的配置文件中进行描述。Falcon故障运维人员的联系方式，在AnyEye的配置文件中描述。

## 自监控的实现

![archi](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20150816/monitor.archi.png)

服务状态定义


自监控巡检






## 自监控服务的部署
AntEye应该和Falcon组件同机房(或者同网络区域)部署，防止跨区域网络问题造成的误报、漏报。如果Falcon散落在多个网络分区，则在每个网络分区部署一个AntEye。

部署在中心集群的Falcon组件往往更重要，其故障需要被实时的发现。因此，可以在中心网络分区部署多套AntEye、监控同一个Falcon集群，实现自监控服务的高可用，如下图。当然，这种高可用，是以运维人员接收重复报警信息为代价的(考虑到报警信息很少，多接收几份也是可以接受的)。

![deploy](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20150816/monitor.deploy.png)

