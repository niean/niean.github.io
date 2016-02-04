---
layout: post
title: Golang闭包问题之小结
date: 2016-02-03 18:00
tags:
  - closure
  - tech
  - golang
---

2015年，因为Golang的闭包问题，频繁的采坑。值此间隙，做一个系统性的小结，希望对大家有所帮助。

## 闭包概述

闭包(Closure)是词法闭包(Lexical Closure)的简称，是为了解决"函数的引用环境可能发生变化"这一问题 而引入的特性。闭包的概念早在高级语言开始发展的年代就产生了，比较靠谱的定义，为: **闭包，是由函数和引用环境(即变量)组合而成的实体，是附有数据的行为**[[1]](http://www.ibm.com/developerworks/cn/linux/l-cn-closure/index.html)。

不同的语言，对闭包的支持形式不尽相同，但基本思想都是一致的。当编程语言满足下述条件时，可以较好的支持闭包特性:

+ 函数是一阶值(First-class value)，即函数可以作为变量、可以作为另一个函数的返回值或参数
+ 支持函数的嵌套
+ 引用环境和函数组合而成的实体，可以被调用
+ 支持匿名函数

闭包优雅的处理了一些棘手的问题，如提高了代码的抽象程度、精简代码等等。但由于引用环境的问题，闭包也会带来了很多的**副作用**，这正是下文的主题:-D

## Golang的闭包
Golang支持匿名函数，这个功能很好的支持了闭包特性。举个例子，来说明Golang闭包的典型做法，如下，

```golang
package main
import "fmt"

func intSeq() func() int {
	i := 0
	return func() int {
		i += 1
		fmt.Printf("%d, %d\n", i, &i)
		return i
	}
}

func main() {
	nextInt := intSeq()
	nextInt()
	nextInt()
	nextInt()

	fmt.Println()
	newInts := intSeq()
	newInts()
}

```

运行结果，如下(将上述代码，保存为文件`closures.go`)，

```golang
$ go run closures.go
1, 0xc20800a200
2, 0xc20800a200
3, 0xc20800a200

1, 0xc20800a288

```

函数`intSeq`，定义了一个匿名函数，并把它作为返回值。作为返回值的函数，捕获了一个内部引用变量`i`，从而构成了一个闭包。

在`main`函数中，我们首先定义了一个函数变量`nextInt`。`nextInt`会捕获变量`i`的取值现场(0)、**另存为**自己的私有数据(初始值为0)，后续每次调用`nextInt`时 都会更新其私有数据内容(0 -> 1 -> 2 -> 3)、私有数据的地址不发生变化(始终为`0xc20800a200`)。

每次调用`intSeq`产生的闭包实例，其引用环境都是私有的、不受其他实例影响的。从`newInts`上面，可以验证上述结论：`newInts`的私有数据地址为`0xc20800a288`、取值不受`nextInt`影响。

## Golang闭包的副作用
闭包带来了代码层面的灵活性，却也因为**引用**导致了一些副作用。特别的，当对引用环境理解不够、处理不当时，会产生意想不到的错误。下面，就是我采过的坑:-(

```golang
func pit() {
	for i := 0; i < 3; i++ {
		go func() {
			fmt.Printf("%d ", i)
		}()
	}
	// Output: 3 3 3
}

```

上面的代码，我们期盼的输出为`0 1 2`，结果却是`3 3 3`，这就是闭包带来的副作用。回避这个副作用的办法，有（1）通过函数的参数传值 或（2）在闭包内构造临时变量:

```golang
// 方法1: 通过函数的参数传值
func pitFix1() {
	for i := 0; i < 3; i++ {
		go func(num int) {
			fmt.Printf("%d ", num)
		}(i)
	}
	// Output: 0 1 2
}

// 方法2: 在闭包内构造临时变量num
func pitFix2() {
	for i := 0; i < 3; i++ {
		num := i
		go func() {
			fmt.Printf("%d ", num)
		}()
	}
	// Output: 0 1 2
}

```

## 小结
如"闭包"一样的语言特性，带来灵活性的同时 往往伴随着一个个的坑。没有完美的设计。

![chrysanthemum.jpg](https://raw.githubusercontent.com/niean/niean.common.store/master/images/front-cover/chrysanthemum.jpg)
