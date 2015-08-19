---
layout: post
title: 小米监控系统Falcon自监控实践
date: 2015-08-16 18:00
tags:
  - falcon
---

监控系统，通常被用于监控其他系统的状态。那么，监控系统的状态，怎么来监控？

我们把对监控系统的监控，称为监控系统的自监控。自监控的需求，没有超出监控的业务范畴。同其他系统一样，监控系统的自监控要做好两方面的工作: 故障报警和状态展示。故障报警，要求尽量实时的发现故障、及时的通知负责人，要求高可用。状态展示，多用于事前预测、事后追查，实时性、可用性要求 较故障报警 低一个量级。下面我们从故障报警和状态展示这两个方面，来介绍小米监控系统Falcon在自监控方面的一些实践经验。

## 故障报警
故障报警相对简单。我们使用第三方监控系统[AntEye](https://github.com/niean/anteye)，来监控Falcon各组件实例的健康状况。

Falcon各个组件，都会提供一个描述自身服务可用性的自监控接口(系统设计之初 就应该考虑到自监控的需求)，描述如下。AntEye服务会定时巡检、主动调用Falcon各实例的自监控接口，如果发现某个实例的接口没有如约返回"ok"，就认为这个组件故障了(约定)，就通过短信、邮件等方式 通知相应负责人员。为了减少报警通知的频率，AntEye采用了简单的退避策略，并会酌情合并一些报警通知的内容。

```bash
	# API for my status
	接口URL
		/health 检测本服务是否正常
		
	请求方法
		GET http://$host:$port/health
		$host 服务所在机器的名称或IP
		$port 服务的http.server监听端口
	
	请求参数
		无参数
	
	返回结果(string)
		"ok"（没有返回"ok", 则服务不正常）
		
```

AntyEye组件主动拉取状态数据，通过本地配置加载监控实例、报警接收人信息、报警通道信息等，这样做，是为了缩短报警链路、使故障的发现过程尽量实时&可靠。AntEye组件足够轻量，代码少、功能简单，这样能够保障单实例的可用性；同时，AntEye又是无状态的，能够同时部署多套，进一步保证了自监控服务的高可用。

在同一个网络分区内部署多个AntEye，如下图所示。我们一般不会让AntEye做跨网络分区的监控，因为这样会带来很多网络层面的误报。多套部署，会造成报警通知的重复发送，这是高可用的代价；从我们的实践经验来看，这个重复可以接受。

![deploy](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20150816/monitor.deploy.png)



## 状态展示
状态展示，是将Falcon各组件实例的状态数据，以图形化的形式展示出来。鉴于实时性、可用性要求不高，我们使用Falcon来做状态数据的存储、展示(用Falcon监控Falcon，自举了，呵呵)，剩下的工作就是状态数据的采集了。

Falcon的多数组件，都会提供一个查询自身服务状态数据的接口，描述如下。

```bash
	# API for querying my statistics
	接口URL
		/counter/all 返回所有的状态数据
	
	请求方法
		GET http://$host:$port/counter/all
		$host 服务所在机器的名称或IP
		$port 服务的http.server监听端口
	
	请求参数
		无参数
	
	返回结果(json)
		{
			"msg": "success", // "success"表示请求被成功处理,其他均是失败
			"data":[ // 自身状态数据的list
				//每个状态数据都有一个名称、计数、时间，可能会有Qps
		    	{
            		"Name": "RecvCnt",
            		"Cnt": 6458396967,
            		"Qps": 81848,
            		"Time": "2015-08-19 15:52:08"
        		},
        		...
			]	
		}

```

Falcon的Task组件，通过状态数据API接口，周期性的主动拉取Falcon各实例的状态数据；然后，处理这些状态数据，适配成Falcon要求的数据格式，push给本地的Agent；Agent会将这些数据路由到Falcon。Task组件，通过配置文件中的`collector`项，定义状态数据采集的相关特性，如下

```base
    "collector":{
        "enable": true,
        "destUrl" : "http://127.0.0.1:1988/v1/push", // 适配后的状态数据发送到本地的1988端口(Agent接收器)
        "srcUrlFmt" : "http://%s/counter/all", // 定义数据采集接口的Format, %s将被替换为 $hostname:$port
        "cluster" : [
            // "$module,$hostname:$port"，表示: 地址test.host01:6060对应了一个transfer服务
            // 结合"srcUrlFmt"的配置,可以得到状态数据采集接口 "http://test.host01:6060/counter/all"
            "transfer,test.host01:6060", 
            "graph,test.host01:6071",
            "task,test.host01:8001"
        ]
    }
```

Task做数据适配时，将endpoint设置为数据来源的机器名`$hostname`($hostname为Task采集配置collector.cluster)，将metric设置为原始状态数据的`$Name`和`$Name.Qps`，将tags设置为`module=$module,port=$port,type=statistics,pdl=falcon`($module,$port来自Task的采集配置collector.cluster,其他两项为固定填充), 将数据类型设置为`GAUGE`，将周期设置为Task的数据采集周期。比如，采用了上文配置的Task，将会做如下适配:

```
	# 一条原始状态数据，来自"transfer,test.host01:6060"
	{
    	"Name": "RecvCnt",
    	"Cnt": 6458396967,
    	"Qps": 81848,
    	"Time": "2015-08-19 15:52:08"
   }
	
	# Task适配之后，得到两条监控数据
	{
		"endpoint": "test.host01", // Task配置collector.cluster中的配置项"transfer,test.host01:6060"中的机器名
		"metric": "RecvCnt", // $Name
		"value": 6458396967, // $Cnt
		"type": "GAUGE",	// 自监控的统计数据,都输GAUGE类型
		"step": 60, // Task的数据采集周期
		"tags": "module=transfer,port=6060,pdl=falcon,type=statistics", // 前两个对应于Task的collector.cluster配置项"transfer,test.host01:6060"中的module和port,后两个是固定填充
		...
	},
	{
		"endpoint": "test.host01",
		"metric": "RecvCnt.Qps", // $Name.Qps
		"value": 81848, // $Qps
		"type": "GAUGE",
		"step": 60,
		"tags": "module=transfer,port=6060,pdl=falcon,type=statistics",
		...
	}
```

我们只能向Falcon，push一份状态数据(防止重叠)，因此，每个网络分区中只能部署一个Task实例(这里，同样不应该跨网络分区采集状态数据)。好在，AntEye服务会监控Task的状态，能够及时发现Task的故障，在一定程度上缓解了 状态数据采集服务 的单点风险。

状态数据入Falcon之后，我们就可以定制Screen页面，展示不同组件的状态数据了。如下图，是小米Falcon的状态数据统计页面。定制页面时，需要先找到您关注的counter，这个可以通过dashboard进行搜索。不同组件、不同counter的具体含义，见这里[Falcon自监控.状态数据]()。

![falcon.screen](https://raw.githubusercontent.com/niean/niean.github.io/master/images/20150816/falcon.screen.png)


## 总结
神医难自医，大型监控系统的故障监控，往往需要借助第三方监控系统([AntEye](https://github.com/niean/anteye))。第三方监控系统，越简单、越独立，越好。

吃自己的狗粮，方便运维的系统才能算是好系统。我们尽量，把获取服务状态数据的过程，变得标准化、通用化，使得各个组件能够用统一的接口搞定。我们编写了简单的统计模块[SCounter](https://github.com/niean/gotools/blob/master/proc/counter.go)(Golang)，我们编写了状态数据采集服务[Task](https://github.com/open-falcon/task)。我们获取状态数据的过程还不太优雅、入侵严重；如果您能指点一二，我们将不胜感激。
