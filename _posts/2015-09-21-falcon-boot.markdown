---
layout: post
title: 监控系统Falcon开机启动设置
date: 2015-09-21 13:00
tags:
  - falcon
  - tech
---

为Falcon添加开机启动设置，步骤为：

1. 编写服务控制脚本
2. 添加开机启动

本文的操作环境为CentOS release 6.3 (Final)，其他版本的Linux用户请参考其他资料。

## 编写控制脚本

脚本示例如下，脚本命名为falcond。其作用为: 以work账号，启动监控系统Falcon的transfer服务和gateway服务（根据需要，修改执行账号、启动的服务等）。脚本falcond需要root账号执行。

```bash
#!/bin/bash
# chkconfig: 2345 50 50
# description: falcond, start main service of falcon when reboot
sudo su - work -c "/home/work/open-falcon/transfer/control restart"
sudo su - work -c "/home/work/open-falcon/gateway/control restart"

```

注意事项:

+ chkconfig  & descriotion这两行的注释一定要有，否则chkconfig命令无法识别该脚本
+ falcond会被root账号执行。如果你的服务需要用非root账号启动，需要用`su - loginUser`进行切换
+ 脚本编写完成后，需要将其移动或者软链至目录`/etc/init.d`，并对root账号设置可执行权限


## 添加开机启动
使用chkconfig命令，添加启动项目falcond，然后修改falcond的启动模式，整个操作过程如下。chkconfig的服务名称为falcond，即启动脚本的名称。关于启动模式，可以参考[这里](http://www.cnblogs.com/xiaoluo501395377/archive/2013/04/01/2992755.html)，一般的生产环境选择`3:多开发者模式`即可。

```bash
# add service
[root@sh1-op-mon-tran02 ~]# chkconfig --add falcond
# list my service
[root@sh1-op-mon-tran02 ~]# chkconfig --list falcond
falcond            0:off    1:off    2:on    3:on    4:on    5:on    6:off

# reset mode
[root@sh1-op-mon-tran02 ~]# chkconfig falcond off
[root@sh1-op-mon-tran02 ~]# chkconfig --list falcond
falcond            0:off    1:off    2:off    3:off    4:off    5:off    6:off
[root@sh1-op-mon-tran02 ~]# chkconfig --level 3 falcond on
[root@sh1-op-mon-tran02 ~]# chkconfig --list falcond
falcond            0:off    1:off    2:off    3:on    4:off    5:off    6:off

```

## 开机启动是否有必要
Falcon的中心服务，一般说来，是不需要设置开机启动的。

异常发生在，某个新建IDC。该IDC负责人，悄悄地重启了所有服务器，导致监控的中心服务中断了一个周末。所以，Falcon才搞了一个开机启动设置(被动运维，疼一下才会往前动一动)。

除了这些新建的、不稳定的IDC，我们不会对Falcon服务做开机启动。



