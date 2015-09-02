---
layout: post
title: 小米监控系统Falcon历史数据高可用实践
date: 2015-09-02 12:00
tags:
  - falcon
---

小米监控系统Falcon的历史数据，被存储在单机的Rrd文件中，存在单点问题。为了实现历史数据的高可用，我们进行了一系列实践，整理成下文。

数据高可用，本质上是维护数据副本、实现数据备份。Falcon历史数据备份，有热备份和冷备份两种方式。

## 热备份
热备份，需要实时维护2+份完全一致的数据。

Falcon历史数据，是经由transfer组件、由graph组件保存在本地的Rrd文件中的。一个很自然的想法是，部署两套实例数相同的graph集群，transfer将同一份数据双打至这两个graph集群——数据源相同、数据存储的归档算法一致，两份历史数据是一致的。

热备份需要生产环境的transfer和graph这两个组件协同工作。进行热备份时，需要额外部署一套graph集群，需要修改transfer的配置。这里举个例子。假设你的Falcon系统，未做热备份时，部署情况为:

```bash
	# graph集群
	"cluster": {
   		"graph-01":"falcon.graph01.bj:6070",
      	"graph-02":"falcon.graph02.bj:6070"
   }
	
	# transfer的graph.cluster配置
	"cluster": {
   		"graph-01":"falcon.graph01.bj:6070", 
      	"graph-02":"falcon.graph02.bj:6070"
   }

```

做完历史数据热备份后，部署情况如下。备份集群的实例名称，要和原集群的一致。

```bash
	# graph集群
	"cluster": {
   		"graph-01":"falcon.graph01.bj:6070",
      	"graph-02":"falcon.graph02.bj:6070"
   }
	
	# graph的备份集群
	"cluster": {
   		"graph-01":"falcon.graph11.bj:6070", // 实例名graph-01要和原集群保持一致
      	"graph-02":"falcon.graph12.bj:6070"
   }
	
	# transfer的graph.cluster配置
	"cluster": {
   		"graph-01":"falcon.graph01.bj:6070,falcon.graph11.bj:6070", 
      	"graph-02":"falcon.graph02.bj:6070,falcon.graph12.bj:6070"
   }

```

进行完上述配置后，能够保证，graph实例falcon.graph01.bj和falcon.graph11.bj上的历史数据完全一致、falcon.graph02.bj和falcon.graph12.bj上的历史数据完全一致，两组实例实时互为备份。当实例falcon.graph01.bj出现问题后，可以直接踢掉之、用其备份实例falcon.graph11.bj做替换，迅速恢复服务；然后，再慢慢的处理实例falcon.graph01.bj的故障。


使用热备份，好处是故障恢复迅速、故障恢复操作简单、历史数据无丢失，坏处是 资源消耗大增:(1)graph组件的资源消耗增加100% (2)transfer组件的数据转发压力增加50%。出于成本考虑，我们没有使用热备份的方案。如果Falcon集群规模不大或者公司有财力支持，你可以考虑使用热备份方案。


## 冷备份
冷备份，是定时的、将历史数据备份到远端服务器上。

冷备份主要依赖人肉运维，需要做好规范，否则会很丑陋。我们的做法是: 每日凌晨00:00，使用rsync工具，将各graph实例上的Rrd文件，同步到远端的历史数据备份主机上。

数据冷备份过程，不需要生产环境的Falcon组件参与。这里，仍然用一个例子来说明。假设graph实例有两个实例，历史数据的存储目录如下:

```bash
	# graph集群，及历史数据存储目录
	"cluster": {
   		"graph-01":"falcon.graph01.bj:6070", 
      	"graph-02":"falcon.graph02.bj:6070"
    },
    "rrd": {
   		"storage": "/home/work/data/6070"
    }
   
```

历史数据冷备主机，及冷备数据存放目录，如下。冷备主机，要有足够大的磁盘容量，这样才能放得下足够多的历史数据备份。

```bash
	# 历史数据冷备主机
	falcon.graph.backup01.bj:
		/home/work/data/falcon.graph01.bj/6070  // rsync from falcon.graph01.bj:/home/work/data/6070
		/home/work/data/falcon.graph02.bj/6070  // rsync from falcon.graph02.bj:/home/work/data/6070
		
		/home/work/open-falcon/graph.backup     // 存放 数据冷备相关的脚本

```

我们会在冷备主机上，对各graph实例，发起rsync请求，进行历史数据的冷备（更进一步，需要check冷备数据的可用性）。为此，需要做如下工作:

1. 设置信任关系。rsync使用了ssh通道，需要提前做好免密码的登录认证，使得由冷备主机发起的rsync请求 不需要密码认证
2. 建立数据备份目录。在冷备主机上，建立相应的数据备份目录
3. 复制备份脚本。准备好发起rsync所需要的脚本
4. 添加crontab。在冷备主机上，添加一条crontab，用于周期性的发起数据备份。
5. check冷备数据。对每一份冷备数据，搭建graph -> query -> dashboard链路，用于验证冷备数据的可用性


冷备主机上的crontab任务，定义如下:

```bash
	0 0 * * * cd /home/work/open-falcon/graph.backup && bash backup.sh &>/tmp/graph.backup.log

```

备份脚本如下，包括backup.sh、rsync.sh 和 graph.list，存放在冷备主机的目录`/home/work/open-falcon/graph.backup`下。文件graph.list用于配置graph实例。rsync完成后，脚本会向本地agent发送一组统计数据、说明本次备份成功与否、本次备份耗时多少等信息，方便用户从screen中观察数据备份的状态。

```bash
	# /home/work/open-falcon/graph.backup/backup.sh
	cur_dir=$(cd $(dirname $0)/; pwd)
	data_dir=/home/work/data
	cd $cur_dir

	tmp=$cur_dir/tmp
	list=$cur_dir/graph.list
	rsyncsh=$cur_dir/rsync.sh
	mkdir -p $tmp

	# check
	if [ ! -f $list ]; then
	    echo -e "[error] miss graph list file"
	    exit 1
	fi

	# rsync async
	ts=`date +%s`
	echo -e "[start], $ts"
	for host in `cat $list`;
	do
	    nohup bash $rsyncsh "$host" "$tmp" &>/dev/null &
	    echo -e "rsync $host"
	done
	echo -e "[done] async, `date +%s`"

```

```bash
	# /home/work/open-falcon/graph.backup/rsync.sh
	host=$1
	log_dir=$2
	if [ "X$host" == "X" -o "X$log_dir" == "X" ];then
	    echo -e "bad arg"
	    exit 1
	fi

	# rsync
	start=`date +%s`
	rsync -avz --bwlimit=10000 work@$host:/home/work/data/6070  /home/work/data/$host/ &>$log_dir/rsyncsh.$host.$start.log
	ecode=$?
	end=`date +%s`

	# time.consuming
	tc=`expr $end - $start`

	# statistics
	curl -X POST -d "[{\"metric\":\"graph.backup.status\", \"endpoint\":\"$host\", \"timestamp\":$start, \"step\":86400, \"value\":$ecode, \"counterType\":\"GAUGE\", \"tags\": \"pdl=falcon,service=graph,job=backup\"}, {\"metric\":\"graph.backup.time\", \"endpoint\":\"$host\", \"timestamp\":$start, \"step\":86400, \"value\":$tc, \"counterType\":\"GAUGE\", \"tags\": \"pdl=falcon,service=graph,job=backup\"}]" http://127.0.0.1:1988/v1/push
```

```bash
	# /home/work/open-falcon/graph.backup/graph.list,拷贝时,请删除本行注释
	falcon.graph01.bj
	falcon.graph02.bj
```

为了验证冷备数据的可用性，我们需要搭建一个check链路: `冷备数据 -> graph -> query -> dashboard`。在冷备主机上，针对每一份冷备数据 部署一个graph服务，用于读取这份数据（这样，冷备主机上可能要部署多个graph实例）。query和dashboard，可以部署在冷备主机上，也可以部署在其他机器上；query的graph列表，地址要配置成冷备机上的graph实例地址，名称要配置成"该graph实例"对应的、生产环境的graph实例名称。


上面介绍了这么多，可能还有不清晰的地方。使用冷备方案，除了节省资源，其余全是坏处:(1)存在一个备份周期的数据丢失(2)故障恢复缓慢(3)实现复杂(4)太多人肉等。最终，我们依然选择了数据冷备的方案，呵呵。


## 总结
Falcon历史数据高可用方案的选择，与用户具体需求、资金投入程度等有很大关系，应该视实际情况而定。后续，我们有计划将历史数据存入HBase，可以省去许多高可用、扩容方面的问题。