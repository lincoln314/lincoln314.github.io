# 常规命令

docker save -o yolov5-v6.2.tar yolov5:v6.2


# 误删overlay2

    直接如果误删var/lib/docker/overlay2文件，可以使用暴力的解决方法：直接删除/var/lib下的docker文件夹。再执行命令：
    ```linux
    systemctl restart docker

    ```

# overlay2 常规清理方式：

    docker system prune

# golang docker部署，在没启动容器，进入容器的方式

- 未启动进入容器：

```linux
docker run -it ubuntu /bin/bash
```

- gpu启动容器

```linux
 --gpus all 
```

- `<br/>`https://www.runoob.com/docker/docker-container-usage.html

# 解决CentOS7 docker容器映射端口只监听ipv6的问题

参考，亲测解决问题，但重启后驱动会掉线，要重装驱动，跑run的脚本 `<br/>` https://www.shuzhiduo.com/A/Gkz139nG5R/

# ubuntu 安装docker环境

```linux
sudo apt-get update

sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo systemctl enable docker
sudo systemctl start docker

```

# 容器内部 yum仓库的设置

```linux
在 CentOS/RHEL 系统中，可以使用 yum 包管理器来安装和升级软件包。为了让 yum 能够找到需要的软件包，需要配置相应的仓库信息。

以下是一些常见的 yum 仓库设置方法：

使用 CentOS 官方镜像：将 /etc/yum.repos.d/CentOS-Base.repo 文件备份，并将 /etc/yum.repos.d/CentOS-Base.repo.rpmnew 文件重命名为 CentOS-Base.repo，然后编辑该文件，将 baseurl 和 mirrorlist 设置为指向 CentOS 官方镜像的地址。

使用 EPEL 仓库：EPEL (Extra Packages for Enterprise Linux) 是针对 RHEL/CentOS/Fedora 等发行版提供额外软件包的项目。可以通过下载对应发行版的 EPEL-release 包，然后使用 yum 安装该包即可添加 EPEL 仓库。

使用阿里云镜像源：阿里云为 CentOS/RHEL 等发行版提供了官方的镜像源，可以使用以下命令替换 CentOS 官方镜像源：

bash
# 备份原始 CentOS-Base.repo 文件
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak

** 在容器中 /etc/yum/yum.conf
# 下载 aliyun 的 CentOS-Base.repo 文件
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo

# 清除 yum 缓存
yum clean all 

# 更新 yum 缓存
yum makecache  
无论使用哪种方法，都需要注意以下事项：

在修改 yum 配置文件之前，建议备份原始的文件；
修改配置文件后，需要清除缓存并重新更新 yum 的元数据（metadata），才能使修改生效；
某些第三方仓库可能没有经过官方认证，存在安全风险，在添加时需要慎重考虑。
```
