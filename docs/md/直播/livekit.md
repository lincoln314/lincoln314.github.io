# 安装步骤

docker安装

![1686105370867](image/livekit/1686105370867.png)

Server URL: wss://licon.livekit.com
API Key: APILeHhWtAusbHk
API Secret: uWVOK1L5KYAC9j3jfhmEBSV3sng8hWdpldzCpTnmYWY

Here's a test token generated with your keys: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjIxMDUyNzQsImlzcyI6IkFQSUxlSGhXdEF1c2JIayIsImp0aSI6InRvbnlfc3RhcmsiLCJuYW1lIjoiVG9ueSBTdGFyayIsIm5iZiI6MTY4NjEwNTI3NCwic3ViIjoidG9ueV9zdGFyayIsInZpZGVvIjp7InJvb20iOiJzdGFyay10b3dlciIsInJvb21Kb2luIjp0cnVlfX0.ldiGoPV2Ly3ik611QpOJ6J-V6pKa6ohc_l1n275AoaY

```linux
docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp -v $PWD/livekit.yaml:/livekit.yaml livekit/livekit-server --config /livekit.yaml --node-ip=0.0.0.0
```

# ngixn

```linux

安装 Nginx 的步骤如下：

打开终端并切换到 root 用户。

执行以下命令更新包列表：

apt update
执行以下命令安装 Nginx：

apt install nginx
安装完成后，执行以下命令启动 Nginx 服务：

systemctl start nginx
如果您想在系统启动时自动启动 Nginx 服务，可以执行以下命令：

systemctl enable nginx
现在，您已经成功安装了 Nginx。您可以在浏览器中输入服务器的 IP 地址，即可看到 Nginx 的欢迎页面。


```

## 添加证书

## 添加ssl配置

```xml
  server {
        listen 443 ssl; 
        server_name licon.livekit.com;
        ssl_certificate /data/pkg/ssl/domain.crt; 
        ssl_certificate_key /data/pkg/ssl/domain.key; 
        ssl_session_timeout 5m;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE; 
        ssl_prefer_server_ciphers on;
        location / {
         proxy_pass http://localhost:7880/;
	 proxy_http_version 1.1;
         proxy_set_header Upgrade $http_upgrade;
         proxy_set_header Connection "Upgrade";
        }

```

```java
livekit-cli create-token \
    --api-key APILeHhWtAusbHk  --api-secret uWVOK1L5KYAC9j3jfhmEBSV3sng8hWdpldzCpTnmYWY  \
    --join --room my-first-room --identity user1 \
    --valid-for 24h


livekit-cli load-test --url wss://47.106.181.184 --api-key devkey --api-secret secret \
    --room my-first-room --audio-publishers 10 --subscribers 1000

```

## nginx错误

![1686120719427](image/livekit/1686120719427.png)




> livekit-load-tester --url wss://域名 --api-key 指令key --api-secret 鉴权指令 --room test-room --publishers 1 --subscribers 100 --duration 5m
>
