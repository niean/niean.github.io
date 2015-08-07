---
layout: post
title: 配置.gitignore后不起作用
date: 2015-07-28 18:00
tags:
  - git
---

### 问题现象
忽略设置失效: 在使用Git进行版本控制的时候, 在.gitignore中对某文件进行了忽略配置, 但是提交时依然对该文件执行了提交。


### 问题分析
gitignore机制是为了确保, 没有入缓存库的文件继续被忽略、继续留在缓存库之外, 已入缓存库的文件继续待在缓存库内、不受gitignore的影响。如果你对某文件使用了```git add```命令、将该文件添加到Git暂存库, 然后在.gitignore文件中添加对该文件的忽略配置，此时.gitignore机制对于该文件失效、对该文件的更新可以被提交。

为了解决这个问题, 先使用```git rm --cached```命令、把文件从Git缓存库中移除, 然后再设置.gitignore配置。之后, 对该文件的更新将不被提交。


### 一个例子
这里给一个实际使用的例子。我有一个会员信息管理的web工程[zebra](https://github.com/niean/zebra), 工程下的文件test.info是用来做测试的, 首次提交时, 不小心将它```git add```到了缓存库, 后面对该文件修改时, Git都提示not staged。

```bash
# git status
vagrant@git:~/.go.github/niean/zebra$ git status
Changes not staged for commit:
	modified:   test.info

```

为了忽略文件test.info的更新, 我们需要在.gitignore中添加一条忽略记录test.info, 然后执行删除文件缓存的命令。

```bash
# add .gitignore
vagrant@git:~/.go.github/niean/zebra$ vim .gitignore
vagrant@git:~/.go.github/niean/zebra$ cat .gitignore
test.info
# git rm --cached
vagrant@git:~/.go.github/niean/zebra$ git rm -f --cached test.info

```

进过上述操作, 文件test.info的提交提示消失了。因为修改了.gitignore文件, 所以Git提示其更新。

```bash
# git status
vagrant@git:~/.go.github/niean/zebra$ git status
Changes not staged for commit:
	modified:   .gitignore
```


本文参考了文档[gitignore-spec](http://git-scm.com/docs/gitignore)
