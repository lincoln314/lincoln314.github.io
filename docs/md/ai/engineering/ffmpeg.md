# 命令集合

- 绿幕背景抠图(效果不理想，任务透明了)

```linux
    ffmpeg -i /data/work/dvha/virtural/科技感背景1.jpg -i /data/work/dvha/virtural/motions.mkv -filter_complex "[1:v]chromakey=Green:0.1:0.2[ckout];[0:v][ckout]overlay[out]" -map "[out]" output.mp4

```

# 关于环境

**原生ffmpeg不支持h264的转码**

- h264 环境配置
  经验证ok 👌`<br/>`https://www.jianshu.com/p/3b0291b1ae3b

  **直接利用conda安装xh264 - 已验证通过**

  ```linux
  conda install x264 ffmpeg -c conda-forge

  然后再去conda的bin目录下去查看该可执行程序
  ```

**在配置过程中,由于装过多个环境,造成报错,是环境冲突**

```linux
报错: relocation R_X86_64_32S against `.rodata' can not be used when making a shared object; 

make clean
再重新 make

```

**llvmlite的安装**

https://stackoverflow.com/questions/61475274/runtimeerror-path-failed-executing-please-point-llvm-config-to-the-path-for

**docker使用cuda**

```linux
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | sudo tee /etc/yum.repos.d/nvidia-docker.repo
yum clean expire-cache 
yum install -y nvidia-docker2
systemctl restart docker
```

**参考**`<br/>`https://huaweicloud.csdn.net/63311993d3efff3090b51ffe.html



# 字幕压制 srt edge-tts生成的字幕

字幕生成的字体，需要特殊字体。

[Releases · adobe-fonts/source-han-sans (bing.com)](https://cn.bing.com/search?q=edge-tts+%E5%AD%97%E5%B9%95%E6%96%87%E4%BB%B6&gs_lcrp=EgZjaHJvbWUqBwgCEEUYwgMyBwgAEEUYwgMyBwgBEEUYwgMyBwgCEEUYwgMyBwgDEEUYwgMyBwgEEEUYwgMyBwgFEEUYwgMyBwgGEEUYwgMyBwgHEEUYwgPSAQwyMDg2NjI3NmowajSoAgiwAgE&FORM=ANAB01&PC=LGTS)

ffmpeg -i C:\\Users\\31468\\Downloads\\result1.mp4 -vf "subtitles=cut.srt:fontsdir=os\\:charenc=utf8" -y output11.mp4
