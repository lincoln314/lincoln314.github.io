# python 与 pip的安装

## 多python版本并存，修改软连接，指向
> linux包含2.7，3.6，3.7多个版本，通过软件连去指向不同版本

**参考连接：**
<br>ModuleNotFoundError: No module named ‘pip‘:https://blog.csdn.net/qq_17105473/article/details/120909679

- pip安装失败报错
```python
ModuleNotFoundError: No module named ‘pip
ModuleNotFoundError: No module named ensurepip

通过直接python脚本安装源解决：

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # 下载安装脚本
python get-pip.py
```

- 更换python软连接
</br>参考： https://blog.csdn.net/qq_42887760/article/details/100997264
python软件连更换后，如果已安装pip，则先卸载：`apt-get remove python3-pip`,然后再安装


# anaconda 与jupyter的安装步骤
  亲测有效可用：<br/>https://blog.csdn.net/weixin_42642296/article/details/115045874