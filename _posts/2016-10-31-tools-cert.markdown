---
layout: post
title: 运维平台服务认证子系统
date: 2016-10-31 20:00
tags:
  - tools
---

## 导读
运维平台服务认证系统(简称Cert) 主要解决**多系统间相互调用时的认证问题**。
本文介绍了Cert的需求来源、系统设计、产品形态及后续优化方向，其中系统设计是关键章节。

## 需求描述
现有的SSO机制，只提供了浏览器访问场景下的用户名认证方式。随着自动化程度的加深，API后端认证、验权的需求正在逐渐增多。为降低全局成本，考虑做一个系统认证管理相关的系统。

系统认证，要满足如下几个功能需求：

- 身份认证。提供一套可行的、C端服务系统身份认证机制
- 授权管理。提供一种可行的授权管理方式，包括授予权限、取消权限
- 访问控制。提供简单的黑白名单功能

系统认证管理系统，要求足够简单：初次接入、管理、使用均要简单，并提供自助的操作UI。

## 名词解释

|名词 |含义 |
|:---- |:---- |
|caller | 主调方，即请求的发起方，一般是client端 |
|callee | 被调方，即服务的提供方，一般是server端 |
|skey   | 系统秘钥(secret key)，用于系统身份认证 |
|caller_token | 主调服务的身份认证码，根据caller、skey生成|
|acl    | 访问控制，定义了 哪些caller可以访问本callee |

## 系统设计
#### 设计关键点
- ACL谁来管理：callee管理自己的ACL，即 "服务提供方决定谁可以访问我"
- 白名单谁来管理：caller来管理自己的服务实例白名单，原因如下，
    - 服务实例变更先对频繁，给callee来做白名单管理沟通成本太高
    - 设置完ACL后，callee充分信任caller(公司内部系统值得信任)
- 如何做身份认证：使用token来做caller身份认证，token需满足如下几点，
    - token不能包含秘钥明文
    - token能够预防重放攻击

token的生成算法为：`md5sum($caller, now()%300, $skey)`，能够容忍300秒的时钟同步误差，也能做到300秒级别的重放攻击预防。

```
#!/bin/bash
caller=$1
skey=$2

ts=`date +%s`
deta=`expr $ts % 300`
ts=`expr $ts - $deta`

raw="$ts.$sys.$skey"
token=$(echo -n $raw | md5sum | awk '{print $1}')
echo "Cert caller=${sys},token=${token}"

```

#### 认证逻辑
Cert的认证逻辑如下图，

![arch.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20161031/cert.timeline.png)


为了不影响正常的请求逻辑，Caller访问Callee时的caller、caller_token信息一般放到Http请求的Header中，形如 `Cert caller=${sys},token=${token}`。

为了方便使用，Callee对Cert的支持通常放到Http代码框架中默认实现。

为方便的区分系统用户和普通员工用户，系统用户名称(caller和callee的名称)一般使用 `sys.`开头儿。在运维权限系统中，系统用户和普通员工用户没有区别，可以被授予各种功能或者数据权限。


## 产品形态
![arch.png](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20161031/cert.ui.png)


## 后续优化方向
- 支持callee接口级别的访问控制
