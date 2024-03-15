- 运行时直接同意： 
    ```linux
    echo y | xxx(命令)
    ```
- 在服务器上用变量替换执行命令
    ```linux
    {param}  变量用括号框起来
    ```
- kaggle上在/working/output/下载数据较快，所以用文件夹抱起来，可以打包成zip包，再下载


**nvidia驱动安装**
https://blog.csdn.net/qq_36326332/article/details/109335550

# kaggle 更换python环境

```linux

!conda create -n p310 python=3.10 -y
!sudo rm /opt/conda/bin/python
!sudo ln -s /opt/conda/envs/p310/bin/python3 /opt/conda/bin/python

```

# kaggle中安装docker环境 嘿嘿
