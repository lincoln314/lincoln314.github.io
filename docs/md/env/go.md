# 环境搭建坑

## 包安装
>**报错1：** go mod或者go install 报错parse “GOPROXY=https://goproxy.cn“:first path segment in URL cannot contain colon
**报错2：** go:invalid proxy URL missing scheme: direct
另外，go get命令在创建go mod 后依旧可以支持。


**解决方案：**
```go
go set GOPROXY=https://goproxy.cn  // 不需要双引号，在未爬墙的使用这个
go set GOPROXY=https://goproxy.cn,direct  // 翻墙可以用这个配置

go env // 查看环境变量
 
 ```


 > go.mod file not found in current directory or any parent directory; see 'go help modules'

 **解决方案：**
 ```go
 go mod init modelMG  // 初始化项目

 ```


# go集成tensorflow，使用其api

> github.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto: cannot find module providing package github.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto
某些包找不到

**解决方案：**

```git

1、 git checkout r1.12  // 切换分支

```


****

<br/> 缺少go的一些依赖，分支切换：https://blog.csdn.net/qq_38431572/article/details/103671986

****


# linux为载体，vscode连接做开发

> tensorflow未提供win的C包,准备搭建linux开发环境，在vscode中通过ssh连接到linux

## amazon服务器最开始只支持用 LightsailDefaultKey-ap-southeast-2  这类key文件，不支持用户密码登录



**解决方式**
参考下面两个方式结合解决密码登录问题

- 参考连接
<br/>1、解决Permission denied (publickey): https://blog.csdn.net/yjk13703623757/article/details/114936739
<br/>2、ubuntu14的root密码修改成功，但还是无法用root账户登录：https://blog.51cto.com/u_330478/4916660


```linux
本次配置登录：root@licon123
 // step1
使用root用户登录，输入passwd

/ /step2
vim /etc/ssh/sshd_config 
PasswordAuthentication yes  # 修改参数1

注释PermitRootLogin without-password  
PermitRootLogin yes  # 修改参数2

// step3
service sshd restart   # 重启服务 

```


## 通过vscode连接到linux

<br/>https://blog.csdn.net/u013272009/article/details/104808628?spm=1001.2101.3001.6650.6&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-6-104808628-blog-105980443.pc_relevant_3mothn_strategy_recovery&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-6-104808628-blog-105980443.pc_relevant_3mothn_strategy_recovery&utm_relevant_index=7



## linux 安装protobuf

<br/>linux 安装protobuf:https://www.jianshu.com/p/05e91bb8506f

## 官方tensorflow go的安装步骤
<br/> https://github.com/tensorflow/tensorflow/blob/master/tensorflow/go/README.md