# situ_demo
## The interface of this project:
classify.py->single_detect()
## Useit:
If you want to run realtime police-case
bash
```
python classify.py 
```
If you want to run file-based excel extract
bash
```
python wrapper.py
```

## 打包程序
* 运行命令 pyinstaller -F manager.py
* 会在dist文件夹下生成一个manager的二进制文件，将二进制文件放到部署的文件夹目录下即可

## 部署使用说明
* 在deploy文件夹下，其中pca文件夹下的都是部署文件，每次更新程序，替换相应的文件即可
* 启动程序，运行命令 ./start.sh 即可