---
layout: post
title: FinOps成本管理体系
date: 2023-01-30 19:00
tags:
  - finops
---

## 导读
本文介绍CH的FinOps成本管理体系，描绘完整轮廓，细节放到各Topic文章介绍。主要是针对IT资源成本，不包括人力、营销等成本。

CH是公司名称，下文简称我司。FinOps成本管理体系，后文简称FinOps。


## 文化
我司的商业，是跟随战略。公司通过模仿商业模式、快速入局，再通过做高运营效率、长跑胜出，运营效率生死攸关。

文化制度上，崇尚节俭。创始团队言传身教、制度设计保驾护航，节俭被体现在价值观、组织建设、目标制定等多方面。文化为商业战略服务。

在这样的商业目标、文化制度背景下，IT资源做为常年Top3的支出项、格外受重视，这是滋生FinOps成本管理体系的土壤。


## 场景
FinOps的业务场景(目标)，主要有如下几个：

- 厂商对账：以止损为目标，对照合同、发现厂商的不合理费用，追溯并挽回损失
- 成本管控：以预算为目标，管控内部业务的资源成本，超预算时禁止新增或提升审批等级
- 成本优化：常态运营、手段多样，用更少的资源投入、支撑更多的业务，持续做高ROI


## 组织
![page.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20201118/finops-zuzhi.png)


## 平台
![page.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20201118/zybcost-arch.png)


## 运营


----
以下是文末附加内容，待整理。


## 预算提报
#### 提报流程
![page.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20201118/zybcost-yusuan-tibaoliucheng.png)

#### 预算要点
![page.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20201118/zybcost-yusuan-tibaoyaodian.png)



## 成本优化
成本优化，学名资源效能，遵循解决问题的工程范式: 发现问题 -> 分析问题 -> 抽象模型 -> 度量指标 -> 建设目标 -> 关键路径 -> 组织保障，如下图。

![page.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20201118/zybcost-chengbenyouhua.png)

#### 成本模型
资源成本 = ∑( 单价 * 资源用量) ∝ 单价 * ( 业务量 * 单位业务资源用量 / 资源利用率 ) ∝ 单价 * 单位业务资源用量 / 资源利用率

其中，业务量由公司业态决定，是IT成本不可决策之基础，本模型不加考虑

#### 关键路径
提升资源效能的关键路径，主要有，

- 降单价：集中采购，多云议价、折扣策略；新产品（如AMD、SSD），高性价比资源（如偏远IDC、过保资源），优势产品
    - 硬件每年都有更新换代，及时Follow云厂商新品、控增量治存量很重要
- 提升资源利用率：避免浪费，容量基线管控（如双云冗余）、弹性扩缩（如ServerLess），调度策略优化，在离线混部、潮汐算力利用，程序优化
- 降单位业务资源用量：降效果（如降低拍搜识别率、降低直播码率、降低数据时效、合理外采），控预算（主要是成本委员会机制）

#### 组织保障
任何项目都需要组织保障，组织保障也是多方面的。这里主要有，

- 组织机制：统一商务采购，统一内部云平台，成本委员会，FinOps
- 加强运营：对账和财务监督（止损），常态运营、定期扫除，业务优化专项

#### 注意事项
- 找准方式，明确哪些是运维擅长的
- 数据驱动，决策要有清晰的数据模型
- 做大ROI，抓大放小
- 既要整存量、又要控增量，整存量要沉淀为运营能力、控增量要沉淀为平台能力

大部分成员会把成本优化当做政治任务，只追求做到预算达标，一些措施会被刻意保留下来、应对将来更繁重的优化目标。这种做法，对公司显然是不利的，这其中既有打工人聪明的狡黠、也有老板激励手段的不到位。
