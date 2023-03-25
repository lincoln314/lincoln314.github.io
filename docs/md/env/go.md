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

linux下
export GOPROXY=https://goproxy.io

 
 ```


# install the CLI
bash -c "$(curl -sS https://raw.githubusercontent.com/cortexlabs/cortex/v0.42.1/get-cli.sh)"

# create a cluster
cortex cluster up cluster.yaml

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


# 在装go跟纯tensorflow失败后，放弃，直接用tfgo替代tensorflow，tensorflow源码有部分protoc文件找不到，编译不过。
</br>tfgo:https://github.com/galeone/tfgo


# 更新go的版本
<br/>linux下更新go版本：https://blog.csdn.net/mu_mu_mu_mu_mu/article/details/119068081

# vscode go代码点击不跳转

- 远程连接后要将所有该装的插件都装上
- 需要装go的一些依赖，如果vscode装不上，则去linux机器上去装，可能两边的缓存没同步，go环境没同步
<br/>https://blog.csdn.net/wrzfeijianshen/article/details/106244812#:~:text=1.go%E4%BB%A3%E7%A0%81%E8%B7%B3%E8%BD%AC%E4%B8%80%E6%96%B9%E9%9D%A2%E6%98%AF%E4%BD%A0%E8%A6%81%E6%8A%8A%E6%89%80%E6%9C%89%E7%9A%84%20vscode%20go%20%E6%8F%92%E4%BB%B6%E8%A6%81%E5%AE%89%E8%A3%85%E4%B8%8A%2C%20%E6%96%B9%E6%B3%95%E6%98%AFctrl%2Bshift,%2B%20p%2C%E8%BE%93%E5%85%A5Go%3AInstall%2FUpdate%2C%E5%9B%9E%E8%BD%A6%E4%B9%8B%E5%90%8E%2C%E6%8A%8A%E8%BF%99%E4%BA%9B%E9%83%BD%E9%80%89%E4%B8%AD%E5%AE%89%E8%A3%85.%202020%E5%B9%B4%E4%B9%8B%E5%90%8E%E7%9A%84%2C%E9%83%BD%E4%BC%9A%E9%87%87%E7%94%A8go%20mod%E7%9A%84%E6%96%B9%E5%BC%8F%2C%E8%AF%B7%E4%B8%8D%E8%A6%81%E7%94%A8%E6%97%A7%E6%96%B9%E5%BC%8F%20%E5%8F%AF%E8%83%BD%E9%9C%80%E8%A6%81%E7%BF%BB%E5%A2%99%E7%AD%89%E5%90%84%E7%A7%8D%E9%80%94%E5%BE%84%E4%B8%8B%E8%BD%BD%E6%BA%90%E7%A0%81%2C



# 环境问题
```go
// 初始化go.mod文件
go mod init 项目名称 

// 下载文件
go mod tidy
// 查看环境
go env
```