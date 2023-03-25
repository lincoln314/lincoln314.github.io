# 命令集合
- 绿幕背景抠图(效果不理想，任务透明了)
```linux
    ffmpeg -i /data/work/dvha/virtural/科技感背景1.jpg -i /data/work/dvha/virtural/motions.mkv -filter_complex "[1:v]chromakey=Green:0.1:0.2[ckout];[0:v][ckout]overlay[out]" -map "[out]" output.mp4

```

- 